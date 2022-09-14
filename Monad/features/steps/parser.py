from behave import *

from main import *

@given('we have a formula')
def step_impl(context):
    context.formula = "(2+3)*4"

@when('we give it to the parser')
def step_impl(context):
    context.answer = eval(context.formula)

@then('the parser should give us the answer')
def step_impl(context):
    assert context.answer == Accept(Value(20, None, ""))

@given('we have a formula with a letter')
def step_impl(context):
    context.formula = "(2+a)*4"

@then('the parser should give us an error')
def step_impl(context):
    assert context.answer == NotAccept(Value(0, None, "(2+a)*4"))

@given(u'we have a formula with a division by 0')
def step_impl(context):
    context.formula = "(2+3)*4/(3-3)"

@then(u'the parser should give us an error division by 0')
def step_impl(context):
    assert context.answer == ErrorDivisionByZero(Value(20, None, '/(3-3)'))
