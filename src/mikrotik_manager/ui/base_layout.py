import inspect
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Literal
from nicegui import ui, helpers
from nicegui.client import Client
from fastapi import Request

from nicegui.api_router import APIRouter


class BaseLayout:
    @dataclass
    class Section:
        name: str
        render: Literal["before", "after"]
        position: int
        func: Callable[..., Any]
        signature: inspect.Signature

    def __init__(self):
        self._sections: dict[str, BaseLayout.Section] = {}
        self._finalized = False

    def _get_sections(self, render: Literal["before", "after"]) -> list[BaseLayout.Section]:
        sections = [section for section in self._sections.values() if section.render == render]
        sections.sort(key=lambda s: s.position)
        return sections

    def section(self,
                name: str | None = None,
                render: Literal["before", "after"] = "before",
                position: int | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        if self._finalized:
            raise RuntimeError("Cannot add sections after the layout has been finalized. Eg. after a page has been defined.")

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            nonlocal name

            # if no name is provided, use the function's name
            if name is None:
                name = func.__name__

            # check for duplicate section names
            if name in self._sections:
                raise ValueError(f"Section with name '{name}' is already defined.")

            # create and store the section
            sections = self._get_sections(render)
            self._sections[name] = BaseLayout.Section(name=name,
                                                      render=render,
                                                      position=position if position is not None else 1 if len(sections) == 0 else sections[-1].position + 1,
                                                      func=func,
                                                      signature=inspect.signature(func))
            return func
        return decorator

    def page(self,
             path: str, *,
             title: str | None = None,
             viewport: str | None = None,
             favicon: str | Path | None = None,
             dark: bool | None = ...,  # type: ignore
             language: Language = ...,  # type: ignore
             response_timeout: float = 3.0,
             reconnect_timeout: float | None = None,
             api_router: APIRouter | None = None,
             **kwargs: Any,
             ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        self._finalized = True

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            async def wrapper(*a, **kw) -> Any:
                # getting additional parameters for the decorated function
                request: Request = kw["request"]
                client: Client = kw["client"]

                def map_parameters(s: inspect.Signature) -> dict[str, Any]:
                    _kw = {k: v for k, v in kw.items() if k in s.parameters.keys()}
                    return s.bind(*a, **_kw).arguments

                def add_to_kwargs(name: str, r: Any) -> None:
                    if r is None:
                        return
                    if name in kw:
                        raise ValueError(f"Section '{section.name}' returned a value but the parameter is already set.")
                    kw[section.name] = r

                # calling the 'before' sections
                for section in self._get_sections("before"):
                    # calling the section function
                    before_result = section.func(**map_parameters(section.signature))

                    # if the section function is a coroutine, await its result
                    if helpers.is_coroutine_function(section.func):
                        before_result = await before_result

                    # adding the result to the possible kwargs for the next functions
                    add_to_kwargs(name=section.name, r=before_result)

                # calling the original function
                result = func(**map_parameters(signature))

                # if the original function is a coroutine, await its result
                if helpers.is_coroutine_function(func):
                    result = await result

                # adding the result to the possible kwargs for the next functions
                add_to_kwargs(name="body", r=result)

                # calling the 'after' sections
                for section in self._get_sections("after"):
                    # calling the section function
                    after_result = section.func(**map_parameters(section.signature))

                    # if the section function is a coroutine, await its result
                    if helpers.is_coroutine_function(section.func):
                        after_result = await after_result

                    # adding the result to the possible kwargs for the next functions
                    add_to_kwargs(name=section.name, r=after_result)

                return result

            # backup of signature of the original function
            signature = inspect.signature(func)

            parameters = list(signature.parameters.values())

            # ensuring 'request' and 'client' are in the parameters
            if "request" not in {p.name for p in parameters}:
                parameters.insert(0,
                                  inspect.Parameter("request",
                                                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                                    annotation=Request))
            if "client" not in {p.name for p in parameters}:
                parameters.insert(0,
                                  inspect.Parameter("client",
                                                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                                    annotation=Client))

            # removing parameters that are provided by sections
            for section in self._sections.values():
                parameters = [p for p in parameters if p.name != section.name]

            # replacing the signature of the wrapper
            wrapper.__signature__ = inspect.Signature(parameters)

            # registering the page with nicegui
            ui.page(path=path,
                    title=title,
                    viewport=viewport,
                    favicon=favicon,
                    dark=dark,
                    language=language,
                    response_timeout=response_timeout,
                    reconnect_timeout=reconnect_timeout,
                    api_router=api_router,
                    **kwargs)(wrapper)
            return func

        return decorator
