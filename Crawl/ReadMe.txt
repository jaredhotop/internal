#Documentation for Web Crawler
#Written by: Jayson Scruggs
#Property of Buchheit

Use:

This program is intended to extract pricing data from competitor
websites in a timely and respectful fashion.

This documentation will use <text> to represent values that should be defined by the user


Adding competitors:

    Competitors should be added to the stores.py file.
    To create a competitor define a function by adding the line:
        def <competitor name>(obj):

    Now define 3 dictionaries that contain the key/value pairs of css_selectors and attributes to be retrieved respectively.
    These dictionaries should be for pricing selectors, sales selectors, and broken link selectors respectively:


            price_selectors = {"<css selector>":"<attribute //This will usually be: innerHTML>"}
            css_selectors = {"css_selector":"attribute"}
            broken_link_selectors = {"<css_selector":"attribute"}

    as we begin making calls to other functions we'll wrap statements in try/except statements:
        try:
            obj.pricing(price_selectors,sale_selectors,broken_link_selectors,<loc_ins  -if competitor is location dependent>)
        except:
            obj.log("Failed to acquire pricing data")
        finally:
            obj.kill_driver()

    /* This code tries to execute the pricing function using the 3 dictionaries we created earlier as arguments  */
    /* These dictionaries must be passed in in this order or with appropriate labeling which we won't cover here */
    /* If the pricing function should fail we wouldn't want our program to stop so we tell it instead to log that*/
    /* error with the provided logging function of our entry object. Regardless of how the rest of our code runs */
    /* we still want to ensure that the driver is still properly closed so we call that function in the "finally"*/
    /* block. If we need to define third party or out of stock functions (these must be custom) then they should */
    /* should be placed in their own try/except blocks before the finally statement.                             */


    To ensure that the function we defined is called we need to add it to the "crawl" method in entry_class.py. Simply follow the format already in place.
    Use the competitor id as the key and stores.<function name> as the value. To the effect of:

                    ...
                    44 : stores.shelper,
                    <competitor id>: stores.<function name>,
                    73 : stores.tsc,
                    ...

    Location based competitors:

    To acquire pricing data on a location basis, more information must be given to the pricing function. If there is
    more than one comp id for this competitor, start by creating an if block above the dictionaries we made earlier.
        if obj.comp_id == <comp id number>
            loc_ins = "<special instructions go here>"
        elif obj.comp_id == <comp id number>
            loc_ins = "<special instructions go here>"
        else obj.comp_id == <comp id number>
            loc_ins = "<special instructions go here>"


    /* This block dictates what special instructions will be used at each location. loc_ins will be passed into  */
    /* the pricing function as a fourth parameter. It is then evaluated as code. The most effective use of this  */
    /* method is to have a function created in loc_data.py that will handle the competitor in question when given*/
    /* a store id or zipcode. More elaborate instructions can be passed using a doc string but this should be    */
    /* avoided if at all possible. Ideally loc_ins = "loc_data.<comp func name>(obj,<zipCode or store id>)"      */


    Lastly a function should be defined in loc_data.py to receive the instructions. This can be tricky as this function
    will probably heavily rely on selenium. Helpful hints:

    --> After declaring your function assign driver = obj._driver to make copied and pasted code work mostly out of the box

    --> Use: "WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "<css id>"))) " to wait for an element to be present on the page

    --> Use: "WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "<css id>")))" to wait for an element to be visible

    --> More detailed information can be found in the selenium documentation: http://selenium-python.readthedocs.io/
Methods:

    This is a brief overview of helpful functions that abstract away the use of selenium functions and required logic for creating valid output
    This will not cover all the functions that exist

    pricing(price_dict,sale_dict = None,broken_dict = None,loc_ins = None):
            This is the main method you should use. It will retrieve the selectors given to it and extract the value of the specified attribute.
            It will do this for both price and sales price. It will check for the presence of an attribute in the given selector for broken links.
            It also has the ability to execute strings of commands that are passed it. This allows for greater flexibility but also presents a risk
            that bad commands can create problems. This ability should be used with care.
            **This method creates the webdriver and puts the URL. It should be called before any method relying on the driver.

            The parameters you must pass:
              A dictionary of pricing css selectors as keys and corresponding attributes as values

            The parameters you can pass:
              A dictionary of sales pricing selectors as keys and corresponding attributes as values
              A dictionary of broken link css selectors as keys and corresponding attributes as values. Additionally text you would like to validate appears
                within the pulled attribute can be appended by concatenating the attribute + '|||' + text. i.e. "innerHTML|||Unavailable"
                *Note the text appended in this way is case sensitive
              A string or docstring containing lines of code to be executed. These commands are executed after driver creation but before the URL is pulled.

            Order of operations:
              Driver creation
              special instructions execution
              URL pulled
              Pricing data retrieved
              sales data retrieved
              broken links flagged

            Returned values:
              None

            Set values:
              _driver
              shop_date
              comp_price
              comp_sale_price
              _broken_flag

    _find_data(select,value):
            This method is primarily used by the pricing method to identify broken links. It is useful for identifying if something exist on the page.
            This method returns a boolean True or False indicating whether the conditions were found or not.

            The parameters you must pass:
              A css selector as a string.

            The parameters you can pass:
              An attribute to be found on the css selector, if this is not specified it will default to innerHTML
              A string to be checked whether or not it appears in the checked attribute.
              *These conditions should be passed together by concatenating the attribute + '|||' + text. i.e. "innerHTML|||Unavailable"

            Example use:
                obj._find_data("span#price","innerHTML|||In Stock")

            Returned Values:
              Boolean - True if the selector and attribute are found (and the value specified is matched)

    _retrieve_data(selector, value):
              This function pulls the specified selector and attribute and returns the data within. This is useful for retrieving a value or grabbing an
              object of the page for selenium manipulation without needing to invoke selenium directly.

            Parameters you must pass:
                  A css selector as a string

            Parameters you can pass:
                  An attribute to be found on the css selector, if this is not specified then the object referenced by the selector will be Returned

            Example use:
                  obj._retrieve_data("span#price","innerText")

            Returned Values:
                  Given an attribute:
                        value of the attribute - if attribute is found.
                        empty string - if attribute is not found
                  Given only selector:
                        The selenium object referenced by selector - if selector is found
                        empty string - if selector is invalid

    set_third_party(bool_val):
              This method sets the comp_shop_third_party attribute and adjust the comp_match_id values.
              As a general rule this method should be called only to set third party = True. It can be called with a parameter of False to set third party to False
              but this does not reverse any changes made to comp_match_id and is equivalent to adjusting the comp_shop_third_party manually and logging the action
              to console.

            Example use:
                If <some condition to determine the link to be third party>:
                      obj.set_third_party()

            Returned Values:
                None

            Set values:
                comp_shop_third_party
                comp_match_id

    set_out_of_stock():
              This method is used to set the value of comp_shop_out_of_stock to True. It is equivalent to changing the value manually and logging the action to console.

              Example use:
                  If <some condition to determine the link to be out of stock>:
                      obj.set_out_of_stock()

              Returned Value:
                  None

              Set values:
                  comp_shop_out_of_stock
