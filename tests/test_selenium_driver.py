from uitesting_gpt.drivers.selenium_wrapper import SeleniumWrapper


def test_create_selenium_driver():
    od = '''Go to Baidu.com
			Find all text boxes.
			Find the first visible text box.
			Click on the first visible text box.'''
    selenium_wrapper = SeleniumWrapper(operation_description=od)
    print(selenium_wrapper.code_compiler.action_output)