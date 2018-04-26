from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import loc_data
import aux_func


def academy(obj):
    price_selectors = {"input#dlItemPrice":"value",}
    sale_selectors = {"span#currentPrice":"innerHTML",}
    broken_link_selectors = {"p#search_results_total_count":"innerHTML"}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to aquire pricing data")
    #No third party
    #check out of stock
    try:
        try:
            oos = obj._driver.find_element_by_css_selector("button#add2CartBtn").get_attribute("innerHTML")
        except:
            oos = "in stock"
        if "Out of Stock" in oos:
            obj.set_out_of_stock()
    except:
        obj.log("Out of stock check failed")
    finally:
        obj.kill_driver()
    return

def acehardware(obj):
    price_selectors = {"div.productPrice span script":"innerHTML",}
    try:
        obj.pricing(price_selectors)
    except:
        obj.log("Failed to aquire pricing data")
    #No third party
    #No out of stock
    finally:
        obj.kill_driver()
    return

def autozone(obj):
    price_selectors = {"table.part-pricing-info td.price.base-price" : "innerText",}
    sale_selectors = {"span.price.light-gray>strong":"innerHTML"}
    broken_link_selectors = {"":""}
    loc_ins="loc_data.autozone(self)"
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
    except:
        obj.log("Failed to acquire pricing data")
    #No third party
    #out of stock check
    try:
        if obj._find_data("div.button-bar-msg-out-of-stock","innerText|||Not Available"):
            obj.set_out_of_stock()
    except:
        obj.log("out of stock check failed")

    finally:
        obj.kill_driver()
    return

def basspro(obj):
    loc_ins = """
bpsku = loc_data.basspro(obj)
for p,value in price_dict.iteritems():
price_dict[p.format(bpsku)] = price_dict.pop(p)
for p,value in sale_dict.iteritems():
sale_dict[p.format(bpsku)] = sale_dict.pop(p)"""
    price_selectors = {"span#listPrice_{}.old_price":"innerHTML",\
    "span#offerPrice_{} > span":"innerHTML","div[itemprop=offers]>span[itemprop=price]":"content"}
    sale_selectors = {"span#offerPrice_{}.price.sale > span":"innerHTML"}
    broken_link_selectors = {"":""}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
    except:
        obj.log("Failed to acqure pricing data")
    finally:
        obj.kill_driver()
    return

def blain(obj):
    price_selectors = {"meta[itemprop=lowprice]":"content",\
    "div.active-price>div.price>span":"innerHTML",\
    "div.original-price>span.price>span":"innerHTML"}
    sale_selectors = {"div.active-price.promo > div.price > span:not([class])":"innerHTML",}
    broken_link_selectors = {"div.list-header-text > span":"innerHTML"}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to acquire pricing data")
    #No third party
    try:
        if not obj._find_data("span.stock-msg.in-stock"):
            obj.set_out_of_stock()
    except:
        obj.log("Out of stock check failed")
    finally:
        obj.kill_driver()
    return

def bootbarn(obj):
    price_selectors = {"span.price-original.price-holder-alt":"innerHTML",\
    "h6.product-callout-title > strong":"innerHTML"}
    sale_selectors = {"h6.product-callout-title > strong":"innerHTML"}
    broken_link_selectors = {"":""}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to aquire pricing data")
    #no third Party
    #no out of stock
    finally:
        obj.kill_driver()
    return

def cabela(obj):
    price_selectors = {"dd.regularnprange":"innerHTML",\
    "div.price > dl > dd.nprange":"innerHTML",\
    "div.price > dl > dd.prange":"innerHTML"}
    sale_selectors = {"dd.saleprice":"innerHTML"}
    broken_link_selectors = {"":""}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to acquire pricing data")
    finally:
        obj.kill_driver()
    return

def Chewy(obj):
    price_selectors = {"span.ga-eec__price" : "innerHTML",}
    sale_selectors = {"p.autoship-pricing" : "innerHTML"}
    broken_link_selectors = {"":""}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        raise
        obj.log("Failed to acquire pricing data")
    #No third party
    try:
        if obj._find_data("div#availability span.unavailable"):
            obj.set_out_of_stock()
    except:
        obj.log("Out of Stock check failed")
    finally:
        obj.kill_driver()
    return

def dickeybub(obj):
    price_selectors = {"p.price > del > span.woocommerce-Price-amount.amount" : "innerHTML",\
    "p.price > span.woocommerce-Price-amount.amount" : "innerHTML",}
    sale_selectors = {"p.price > ins > span.woocommerce-Price-amount.amount" : "innerHTML",}
    try:
        obj.pricing(price_selectors,sale_selectors,)
    except:
        obj.log("Failed to acquire pricing data")
    finally:
        obj.kill_driver()
    return

def farm_and_home(obj):
    obj.log("Competitor: %d not yet defined" %obj.comp_id)
    obj.set_undefined()
    return

def home_depot(obj):
    if obj.comp_id == 23:
        loc_ins = "loc_data.home_depot(self,62226)"
    elif obj.comp_id == 5:
        loc_ins = "loc_data.home_depot(self,63028)"
    elif obj.comp_id == 17:
        loc_ins = "loc_data.home_depot(self,62650)"
    price_selectors = {"input#ciItemPrice":"value","span#ajaxPriceStrikeThru":"innerHTML","span#ajaxPriceAlt":"innerHTML",\
    "span#ajaxPrice":"content"}
    sale_selectors = {"span#ajaxPrice":"content"}
    broken_link_selectors = {"div.buybelt__flex-wrapper.buybelt__store-wrapper span.u__text--danger":"innerHTML|||Unavailable",\
    "div#productinfo_ctn > div.error >p":"innerHTML|||not currently available"}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
    except:
        obj.log("Failed to acquire pricing data")
        #Out of stock check
    try:
        try:
            if obj._find_data("input#availableInLocalStore","value|||false"):
                obj.set_out_of_stock()
        except:
            try:
                WebDriverWait(obj._driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.buybelt__box")))
                if '0' == str(obj._retrieve_data("span.quantity","innerHTML")):
                    obj.set_out_of_stock()
            except TimeoutException as error:
                pass
    except:
        obj.log("Out of stock check failed")
    finally:
        obj.kill_driver()
    return

def lowes(obj):
    if obj.comp_id == 6:
        loc_ins = "loc_data.lowes(self,63028,'Festus')"
    elif obj.comp_id == 15:
        loc_ins = "loc_data.lowes(self,63701,'Cape Girardeau')"
    elif obj.comp_id == 16:
        loc_ins = "loc_data.lowes(self,62704,'Springfield')"
    elif obj.comp_id == 24:
        loc_ins = "loc_data.lowes(self,62221,'Belleville')"
    price_selectors = {"input[name=productId]":"data-productprice","span.secondary-text.small-type.art-pd-wasPriceLbl":"innerHTML",\
    "span.primary-font.jumbo.strong.art-pd-price":"innerHTML"}
    sale_selectors = {"span.primary-font.jumbo.strong.art-pd-contractPricing":"innerHTML"}
    broken_link_selectors = {"div.alert.alert-warning i.icon-error-outline.red":"",\
    " div.pd-shipping-delivery.met-fulfillment-delivery.grid-50.tablet-grid-50 div.media-body > p":"innerHTML|||unavailable"}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
    except:
        raise
        obj.log("Failed to acquire pricing data")
    #Out of stock check
    try:
        if obj._find_data("div.fulfillment-method div.media-body >p","innerHTML|||Unavailable"):
            obj.set_out_of_stock()
    except:
        obj.log("Out of stock check failed")
    finally:
        obj.kill_driver()
    return

def menards(obj):
    if obj.comp_id == 7:
        loc_ins = "loc_data.menards(self,'3286')"
    elif obj.comp_id == 26:
        loc_ins = "loc_data.menards(self,'3334')"
    elif obj.comp_id == 27:
        loc_ins = "loc_data.menards(self,'3293')"

    price_selectors = {"span.bargainStrike" : "innerHTML",\
    "span.EDLP.fontSize16.fontBold.alignRight" : "innerHTML",\
    "span#totalItemPriceFloater" : "innerHTML",
    "span.finalPriceSpan.leftFloat":"innerText" }
    sale_selectors = {"span.bargainPrice" : "innerHTML", \
    "span#totalItemPriceFloater" : "innerHTML",
    "span.finalPriceSpan.leftFloat":"innerText"}
    broken_link_selectors = {"h3.resettitle":"innerHTML"}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors,loc_ins)
    except:
        obj.log("Failed to acquire pricing data")
    finally:
        obj.kill_driver()
    return

def orscheln(obj):
    price_selectors = {"span.product_unit_price" : "innerHTML","meta[itemprop=price]" : "content"}
    sale_selectors = {"":""}
    broken_link_selectors = {"":""}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to acquire pricing data")
    #No third party
    #No out of stock
    try:
        if obj._find_data("div.product-info-stock-sku","innerHTML|||Out of Stock Online"):
            obj.set_out_of_stock()
    except:
        obj.log("Out of Stock check failed")
    finally:
        obj.kill_driver()
    return

def petsense(obj):
    obj.log("Competitor: %d not yet defined" %obj.comp_id)
    obj.set_undefined()
    return
    price_selectors = {"div#product_price span.money" : "innerHTML",}
    sale_selectors = {"":""}
    broken_link_selectors = {"div.selector-wrapper>select.single-option-selector":"innerHTML"}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to acquire pricing data")
    #No third party
    #No out of stock
    finally:
        obj.kill_driver()
    return

def ruralking(obj):
    price_selectors = {"span.price" : "innerHTML","meta[itemprop=price]":"content",}
    #"span[itemprop=offers] > span[itemprop=price]":"innerHTML"}
    sale_selectors = {"":""}
    broken_link_selectors = {"div.page-head-alt >h3":"innerHTML|||Sorry"}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to acquire pricing data")
    try:
        if "OUT OF STOCK" in obj._retrieve_data("div.product-shop h1[style]","innerHTML"):
            obj.set_out_of_stock()
        elif obj._find_data("p.prod_availability >span.backorder"):
            obj.set_out_of_stock()
    except:
        obj.log("Out of stock check failed")
    finally:
        obj.kill_driver()
    return
    # sale css_selector? -> div.Price-old.display-inline-block.arrange-fill.font-normal.u-textNavyBlue.display-inline").find_element_by_css_selector("span.Price-group").get_attribute("title"))

def sears(obj):
    price_selectors = {"span.price-wrapper":"innerHTML"}
    sale_selectors = {"h4.redSalePrice span.price-wrapper":"innerHTML"}
    broken_link_selectors = {"":""}
    try:
        obj.pricing(price_selectors,sale_selectors,broken_link_selectors)
    except:
        obj.log("Failed to acquire pricing data")
    #No Third Party
    #No out of Stock
    finally:
        obj.kill_driver()
    return

def shelper(obj):
    price_selectors = {"div.product-content-inner > div.product-price > span.price-original.price-holder-alt > strong" : "innerHTML",}
    sale_selectors = {"div.product-content-inner > div.product-callout > h6.product-callout-title > strong" : "innerHTML",}
    broken_link_selectors = {"":""}
    try:
        obj.pricing(price_selectors,sale_selectors)
    except:
        obj.log("Failed to acquire pricing data")
        #No third party
        #No out of stock
    finally:
        obj.kill_driver()
    return

def tsc(obj):
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
        obj.log("Failed to acquire pricing data")
        #no third party
        #no out of stock
    finally:
        obj.kill_driver()
    return

def valleyvet(obj):
    obj.log("Competitor: %d not yet defined" %obj.comp_id)
    obj.set_undefined()
    return

def walmart(obj):
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
        obj.log("Failed to aquire pricing data")
    #check for Third party
    try:
        if obj._find_data("span.seller-shipping-msg.font-semibold.u-textBlue"):
                sellers = obj._driver.find_elements_by_css_selector("div.secondary-bot div.arrange.seller-container")
                for sell in sellers:
                    if sell.find_element_by_css_selector("span.seller-shipping-msg.font-semibold.u-textBlue").get_attribute("innerHTML").encode('utf-8') == 'Walmart':
                        obj.set_price(aux_func.clean(sell.find_element_by_css_selector("span.Price-group").get_attribute('title')))
                        break
                else:
                    obj.set_third_party()
        elif not obj._find_data("a.font-bold.prod-SoldShipByMsg[href='http://help.walmart.com']"):
            obj.set_third_party()

    except:
        obj.log("Third party check failed")
    #check Out of stock
    try:
        try:
            oos = obj._driver.find_element_by_css_selector("span.copy-mini.display-block-xs.font-bold.u-textBlack").get_attribute("innerHTML")
        except:
            oos = "in stock"
        if "Out of stock" in oos:
            obj.set_out_of_stock()
    except:
        obj.log("Out of stock check failed")
    finally:
            obj.kill_driver()
    return

def _default(obj):
    obj.log("Unknown Competitor ID")
    obj.set_undefined()
    return
