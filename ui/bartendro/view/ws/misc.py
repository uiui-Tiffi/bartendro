# -*- coding: utf-8 -*-
from werkzeug.utils import redirect
from werkzeug.exceptions import BadRequest, ServiceUnavailable
from bartendro.utils import session, local, expose, validate_url, url_for, render_text
from bartendro.model.drink import Drink
from bartendro.model.booze import Booze
from bartendro.form.booze import BoozeForm

@expose('/ws/reset')
def ws_reset(request):
    driver = local.application.driver
    driver.chain_init()
    driver.led(255, 0, 0, 255)
    mc = local.application.mc
    mc.delete("top_drinks")
    mc.delete("other_drinks")
    mc.delete("available_drink_list")
    return render_text("ok\n")

@expose('/ws/testchain')
def ws_test_chain(request):
    driver = local.application.driver
    for disp in xrange(driver.count()):
        print "test %d" % disp
	if not driver.ping(disp):
	    raise ServiceUnavailable("Error: Dispenser %d failed ping." % disp)
    return render_text("ok\n")

@expose('/ws/checklevels')
def ws_check_levels(request):
    mixer = local.application.mixer
    if not mixer.check_liquid_levels():
        raise ServiceUnavailable("Error: Checking dispenser levels failed.")
    mc = local.application.mc
    mc.delete("top_drinks")
    mc.delete("other_drinks")
    mc.delete("available_drink_list")
    return render_text("ok\n")
