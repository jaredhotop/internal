Documentation for Web Crawler
#
#Written by: Jayson Scruggs
#Property of Buchheit
#

Use:

This program is intended to extract pricing data from competitor
websites in a timely and respectful fashion.

This documentation will use <text> to represent values that should be defined by the user


Adding competitors:

    Competitors should be added to the stores.py file.
    To create a competitor define a function by adding the line:
        def <competitor name>(obj):

    Now define 3 dictionaries that contain the key value pairs of css_selectors and attributes to be retrieved respectively.
    These dictionaries should be for pricing selectors, sales selectors, and broken link selectors respectively:
        price_selectors = {"<css selector>":"<attribute //This will usually be: innerHTML>"}
        css_selectors = {"css_selector":"attribute"}
        broken_link_selectors = {"<css_selector":"attribute"}

    as we begin making calls to other functions we'll wrap statements in try/except statements:
        try:
            obj.pricing(price_selectors,sale_selectors,broken_link_selectors,<loc_ins if competitor is location dependent>)
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

    Location based competitors:

    to acquire pricing data on a location basis more information must be given to the pricing function. If there is
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


    Lastly a function should be defined in loc_data.py to receive the instructions. This can be trick as this function
    will probably heavily rely on selenium. Helpful hints:

    --> After declaring your function assign driver = obj._driver to make copied code work mostly out of the box

    --> Use: "WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "<css id>"))) " to wait for an element to be present on the page

    --> Use: "WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "<css id>")))" to wait for an element to be visible
Methods:
