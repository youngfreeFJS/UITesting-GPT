'''Selenium Driver Wrapper.'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from uitesting_gpt.settings import DEFAULT_GPT_MODLE
from uitesting_gpt.drivers.base_wrapper import BaseWrapper
from uitesting_gpt.llms.testing_code_compiler import TestingCodeCompiler

class SeleniumWrapper(BaseWrapper):
    def __init__(self, operation_description, gpt_model=DEFAULT_GPT_MODLE, verbose=False) -> None:
        '''Initialize the Selenium Wrapper.'''
        self.operation_description = operation_description
        self.gpt_model = gpt_model
        self.verbose = verbose
        self.driver = self.__create_selenium_driver()
        self.BASE_PROMPT = """You have an instance `env` with methods:
                            - `env.driver`, the Selenium webdriver.
                            - `env.get(url)` goes to url.
                            - `env.find_elements(by='class name', value=None)` finds and returns list `WebElement`. The argument `by` is a string that specifies the locator strategy. The argument `value` is a string that specifies the locator value. `by` is usually `xpath` and `value` is the xpath of the element.
                            - `env.find_element(by='class name', value=None)` is like `env.find_elements()` but only returns the first element.
                            - `env.find_nearest(e, xpath, direction="above")` can be used to locate a WebElement that matches the xpath near WebElement e. Direction is "above", "below", "left", or "right".
                            - `env.send_keys(element, text)` sends `text` to element. Be mindful of special keys, like "enter" (use Keys.ENTER) and "tab" (use Keys.TAB).
                            - `env.click(element)` clicks the WebElement. Use this instead of `element.click()`.
                            - `env.wait(seconds)` waits for `seconds`.
                            - `env.scroll(direction, iframe=None)` scrolls. Switches to `iframe` if given. `direction` can be "up", "down", "bottom", "top", "left", or "right".
                            - `env.get_llm_response(text)` asks AI about a string `text`.
                            - `env.query_memory(prompt)` asks AI to query its memory of ALL the web pages it has browsed so far. Invoked with something like "Query memory".
                            - `env.retrieve_information(prompt)` returns a string, information from a page given a prompt. Use prompt="Summarize:" for summaries. Invoked with commands like "retrieve", "find in the page", or similar.
                            - `env.ask_llm_to_find_element(description)` asks AI to find an WebElement that matches the description. It returns None if it cannot find an element that matches the description, so you must check for that.
                            - `env.screenshot(element, filename)` takes a screenshot of the element and saves it to `filename`.
                            - `env.save(text, filename)` saves the string `text` to a file `filename`.
                            - `env.get_text_from_page()` returns the free text from the page.

                            Guidelines for using GPTWebElement:
                            - `element.get_attribute(attr)` returns the value of the attribute of the element. If the attribute does not exist, it returns ''.
                            - `element.find_elements(by='id', value=None)` is similar to `env.find_elements()` except that it only searches the children of the element and does not search iframes.
                            - `env.is_element_visible_in_viewport(element)` returns if the element is visible in the viewport.

                            INSTRUCTIONS:
                            {instructions}

                            Your code must obey the following constraints:
                            - In xpaths, to get the text of an element, do NOT use `text()` (use `normalize-space()` instead), and don't use "normalize-space() = 'text'", use "contains(normalize-space(), 'text')" instead. For instance, the xpath for a button element that contains text is "//button[contains(normalize-space(), 'text')]".
                            - Do NOT use `element.text` to get text. Use `env.get_text_of_element(element)` instead.
                            - Do NOT use `element.send_keys(text)` or `element.click()`. Use `env.send_keys(text)` and `env.click(element)` instead.
                            - Only do what I instruct you to do.
                            - Only write code, no comments.
                            - Has correct indentation.
                            - Respect case sensitivity in the instructions.
                            - Does not call any functions besides those given above and those defined by the base language spec.
                            - You may not import any modules. You may not use any external libraries.

                            OUTPUT: ```python"""
        self.code_compiler = TestingCodeCompiler(gpt_model=gpt_model,
                                                 code_compiler_base_prompt=self.BASE_PROMPT,
                                                 operation_description=self.operation_description)
    def __create_selenium_driver(self):
        '''Create Selenium Driver.
        Initialize Selenium and start interactive session.
        More see: https://selenium-python.readthedocs.io/getting-started.html
        '''
        chrome_options = Options()
        # set chrome window maximized when start.
        chrome_options.add_argument('--start-maximized')
        return webdriver.Chrome(options=chrome_options)
    
    def run(self):
        self.driver.get('http://www.baidu.com')
        
    