import abc
import time
from dataclasses import dataclass

from playwright.sync_api import Page
import typing
from typing import Literal


@dataclass
class BasePage(abc.ABC):
    page: Page
    url = None

    def __wait(self):
        self.page.wait_for_load_state()

    class Elements:
        pass

    def open(self, url: str = None):
        self.page.goto(url or self.url)
        self.__wait()

    @staticmethod
    def sleep(times):
        time.sleep(times)

    def get_title(self):
        self.__wait()
        return self.page.title()

    def check_page_contains_text(self, *texts):
        self.__wait()
        errors = []
        for text in texts:
            xpath = f"//body//*[contains(normalize-space(.), '{text}')]"
            visible_list = list(filter(lambda x: x.is_visible() is True, self.page.locator(xpath).all()))
            if len(visible_list) == 0:
                errors.append(text)
        assert len(errors) == 0, f"Текст '{errors}' не найден на странице"

    def on(self, event: str, f: typing.Callable[..., None]) -> None:
        return self.page.on(event=event, f=f)

    def execute_js(self, script, arg=None):
        return self.page.evaluate(script, arg)
