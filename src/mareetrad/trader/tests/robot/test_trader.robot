# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s mareetrad.trader -t test_trader.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src mareetrad.trader.testing.MAREETRAD_TRADER_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_trader.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a trader
  Given a logged-in site administrator
    and an add trader form
   When I type 'My Trader' into the title field
    and I submit the form
   Then a trader with the title 'My Trader' has been created

Scenario: As a site administrator I can view a trader
  Given a logged-in site administrator
    and a trader 'My Trader'
   When I go to the trader view
   Then I can see the trader title 'My Trader'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add trader form
  Go To  ${PLONE_URL}/++add++trader

a trader 'My Trader'
  Create content  type=trader  id=my-trader  title=My Trader


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the trader view
  Go To  ${PLONE_URL}/my-trader
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a trader with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the trader title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
