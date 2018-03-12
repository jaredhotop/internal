from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import loc_data


def _academy(obj):
	price_selectors = {"input#dlItemPrice":"value",}
	sale_selectors = {"span#currentPrice":"innerHTML",}
	broken_link_selectors = {"p#search_results_total_count":"innerHTML"}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to aquire pricing data")
	#No third party
	#check out of stock
	try:
		try:
			oos = obj.driver.find_element_by_css_selector("button#add2CartBtn").get_attribute("innerHTML")
		except:
			oos = "in stock"
		if "Out of Stock" in oos:
			obj.set_out_of_stock()
	except:
		obj._log("Out of stock check failed")
	finally:
		obj._kill_driver()
	return

def _acehardware(obj):
	price_selectors = {"div.productPrice span script":"innerHTML",}
	try:
		obj.pricing(price_selectors)
	except:
		obj._log("Failed to aquire pricing data")
	#No third party
	#No out of stock
	finally:
		obj._kill_driver()
	return

def _basspro(obj):
	loc_ins = """
bpsku = loc_data.basspro(obj)
for p,value in price_dict.iteritems():
price_dict[p.format(bpsku)] = price_dict.pop(p)
for p,value in sale_dict.iteritems():
sale_dict[p.format(bpsku)] = sale_dict.pop(p)"""
	price_selectors = {"span#listPrice_{}.old_price":"innerHTML",\
	"span#offerPrice_{} > span":"innerHTML"}
	sale_selectors = {"span#offerPrice_{}.price.sale > span":"innerHTML"}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
	except:
		obj._log("Failed to acqure pricing data")
	finally:
		obj._kill_driver()
	return

def _blain(obj):
	price_selectors = {"meta[itemprop=lowprice]":"content",\
	"div.active-price>div.price>span":"innerHTML",\
	"div.original-price>span.price>span":"innerHTML"}
	sale_selectors = {"div.active-price.promo > div.price > span:not([class])":"innerHTML",}
	broken_link_selectors = {"div.list-header-text > span":"innerHTML"}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to acquire pricing data")
	#No third party
	try:
		if not obj._find_data("span.stock-msg.in-stock"):
			obj.set_out_of_stock()
	except:
		obj._log("Out of stock check failed")
	finally:
		obj._kill_driver()
	return

def _bootbarn(obj):
	price_selectors = {"span.price-original.price-holder-alt":"innerHTML",\
	"h6.product-callout-title > strong":"innerHTML"}
	sale_selectors = {"h6.product-callout-title > strong":"innerHTML"}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to aquire pricing data")
	#no third Party
	#no out of stock
	finally:
		obj._kill_driver()
	return

def _cabela(obj):
	price_selectors = {"dd.regularnprange":"innerHTML",\
	"div.price > dl > dd.nprange":"innerHTML"}
	sale_selectors = {"dd.saleprice":"innerHTML"}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to acquire pricing data")
	finally:
		obj._kill_driver()
	return

def _dickeybub(obj):
	price_selectors = {"p.price > del > span.woocommerce-Price-amount.amount" : "innerHTML",\
	"p.price > span.woocommerce-Price-amount.amount" : "innerHTML",}
	sale_selectors = {"p.price > ins > span.woocommerce-Price-amount.amount" : "innerHTML",}
	try:
		obj.pricing(price_selectors,sale_selectors,)
	except:
		obj._log("Failed to acquire pricing data")
	finally:
		obj._kill_driver()
	return

def _home_depot(obj):
	if obj.comp_id == 23:
		loc_ins = "loc_data.home_depot(self,62226)"
	elif obj.comp_id == 5:
		loc_ins = "loc_data.home_depot(self,63028)"
	elif obj.comp_id == 17:
		loc_ins = "loc_data.home_depot(self,62650)"
	price_selectors = {"span#ajaxPriceStrikeThru":"innerHTML","span#ajaxPriceAlt":"innerHTML","span#ajaxPrice":"content"}
	sale_selectors = {"span#ajaxPrice":"content"}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
	except:
		raise
		obj._log("Failed to acquire pricing data")
	try:
		WebDriverWait(obj.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.buybelt__box")))
		if '0' in obj._retrieve_data("span.quantity","innerHTML"):
			obj.set_out_of_stock()
	except:
            raise
            obj._log("Out of stock check failed")
	finally:
		obj._kill_driver()
	return

def _farm_and_home(obj):
	obj._log("Competitor: %d not yet defined" %obj.comp_id)
	obj.set_undefined()
	return

def _lowes(obj):
	if obj.comp_id == 6:
		loc_ins = "loc_data.lowes(self,63028)"
	elif obj.comp_id == 15:
		loc_ins = "loc_data.lowes(self,63701)"
	elif obj.comp_id == 16:
		loc_ins = "loc_data.lowes(self,62704)"
	elif obj.comp_id == 24:
		loc_ins = "loc_data.lowes(self,62221)"
	price_selectors = {"span.secondary-text.small-type.art-pd-wasPriceLbl":"innerHTML",\
	"span.primary-font.jumbo.strong.art-pd-price":"innerHTML"}
	sale_selectors = {"span.primary-font.jumbo.strong.art-pd-contractPricing":"innerHTML"}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
	except:
		obj._log("Failed to acquire pricing data")
	finally:
		obj._kill_driver()
	return

def _menards(obj):
	if obj.comp_id == 7:
		loc_ins = "loc_data.menards(self,'3286')"
	elif obj.comp_id == 26:
		loc_ins = "loc_data.menards(self,'3334')"
	elif obj.comp_id == 27:
		loc_ins = "loc_data.menards(self,'3293')"

	price_selectors = {"span.bargainStrike" : "innerHTML",\
	"span.EDLP.fontSize16.fontBold.alignRight" : "innerHTML",\
	"span#totalItemPriceFloater" : "innerHTML"}
	sale_selectors = {"span.bargainPrice" : "innerHTML", \
	"span#totalItemPriceFloater" : "innerHTML"}
	broken_link_selectors = {"h3.resettitle":"innerHTML"}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
	except:
		obj._log("Failed to acquire pricing data")
	finally:
		obj._kill_driver()
	return

def _orscheln(obj):
	price_selectors = {"span.product_unit_price" : "innerHTML",}
	sale_selectors = {"":""}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to acquire pricing data")
	#No third party
	#No out of stock
	finally:
		obj._kill_driver()
	return

def _ruralking(obj):
	price_selectors = {"div.price-box > span.regular-price > span.price":"innerHTML"}
	sale_selectors = {"":""}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to acquire pricing data")
	try:
		time.sleep(5)
		obj.driver.get_screenshot_as_file(os.path.expanduser("~/Documents/%s.png" %obj.sku))
		if "OUT OF STOCK" in obj._retrieve_data("div.product-shop h1[style]","innerHTML"):
			obj.set_out_of_stock()
	except:
		pass
	finally:
		obj._kill_driver()
	return
	# sale css_selector? -> div.Price-old.display-inline-block.arrange-fill.font-normal.u-textNavyBlue.display-inline").find_element_by_css_selector("span.Price-group").get_attribute("title"))

def _sears(obj):
	price_selectors = {"span.price-wrapper":"innerHTML"}
	sale_selectors = {"h4.redSalePrice span.price-wrapper":"innerHTML"}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to acquire pricing data")
	#No Third Party
	#No out of Stock
	finally:
		obj._kill_driver()
	return

def _shelper(obj):
	price_selectors = {"div.product-content-inner > div.product-price > span.price-original.price-holder-alt > strong" : "innerHTML",}
	sale_selectors = {"div.product-content-inner > div.product-callout > h6.product-callout-title > strong" : "innerHTML",}
	broken_link_selectors = {"":""}
	try:
		obj.pricing(price_selectors,sale_selectors)
	except:
		obj._log("Failed to acquire pricing data")
		#No third party
		#No out of stock
	finally:
		obj._kill_driver()
	return

def _tsc(obj):
	#view in cart item
	# https://www.tractorsupply.com/tsc/product/jonsered-502cc-gas-chainsaw-cs2250s?cm_vc=-10005
	if obj.comp_id == 73:
		loc_ins = "loc_data.tsc(self,'63049')"
	elif obj.comp_id == 74:
		loc_ins = "loc_data.tsc(self,'63701')"
	elif obj.comp_id == 8:
		loc_ins = "loc_data.tsc(self,'63640')"
	elif obj.comp_id == 124:
		loc_ins = "loc_data.tsc(self,'63801')"
	price_selectors = {"span.was_text":"innerHTML","span.dollar_price":"innerHTML"}
	sale_selectors = {"span.dollar_price":"innerHTML"}
	broken_link_selectors = {"div#WC_GenericError_6.info":"innerHTML"}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
	except:
		obj._log("Failed to acquire pricing data")
		#no third party
		#no out of stock
	finally:
		obj._kill_driver()
	return

def _valleyvet(obj):
	obj._log("Competitor: %d not yet defined" %obj.comp_id)
	obj.set_undefined()
	return

def _walmart(obj):
	price_selectors = {"div.Price-old.display-inline-block.arrange-fill.font-normal.u-textNavyBlue.display-inline > span.Price-group" : "title",\
	"div.prod-BotRow.prod-showBottomBorder.prod-OfferSection.prod-OfferSection-twoPriceDisplay div.Grid-col:nth-child(4) span.Price-group" : "title",\
	"span.display-inline-block.arrange-fit.Price.Price-enhanced.u-textNavyBlue > span.Price-group" : "title",\
	"span.display-inline-block.arrange-fit.Price.Price-enhanced.u-textGray > span.Price-group" : "title",}
	broken_link_selectors = {"div.font-semibold.prod-Bot-partial-head" : "innerHTML",\
	"p.error-ErrorPage-copy":"innerHTML"}
	sale_selectors = {}
	try:
		obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
	except:
		obj._log("Failed to aquire pricing data")
	#check for Third party
	try:
		if obj._find_data("span.seller-shipping-msg.font-semibold.u-textBlue"):
				sellers = obj.driver.find_elements_by_css_selector("div.secondary-bot div.arrange.seller-container")
				for sell in sellers:
					if sell.find_element_by_css_selector("span.seller-shipping-msg.font-semibold.u-textBlue").get_attribute("innerHTML").encode('utf-8') == 'Walmart':
						obj.set_price(aux_func.clean(sell.find_element_by_css_selector("span.Price-group").get_attribute('title')))
						break
		elif not obj._find_data("a.font-bold.prod-SoldShipByMsg[href='http://help.walmart.com']"):
			obj.set_third_party()

	except:
		obj._log("Third party check failed")
	#check Out of stock
	try:
		try:
			oos = obj.driver.find_element_by_css_selector("span.copy-mini.display-block-xs.font-bold.u-textBlack").get_attribute("innerHTML")
		except:
			oos = "in stock"
		if "Out of stock" in oos:
			obj.set_out_of_stock()
	except:
		obj._log("Out of stock check failed")
	finally:
			obj._kill_driver()
	return

def _default(obj):
	obj._log("Unknown Competitor ID")
	obj.set_undefined()
	return
