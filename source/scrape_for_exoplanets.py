# import required modules
import time, uuid, pathlib
from tqdm import trange
import pandas as pd

# Import my scraper class
from Scraper import Scraper

# alse, because I prefer this function name
wait = time.sleep

# search for a specific exoplanet using the scraper
def search_exoplanet(scraper, name):
    ''' Use the search feature to find the link for a specific exoplanet. '''
    # go to the webpage
    scraper.navigate("https://exoplanets.nasa.gov/discovery/exoplanet-catalog/")
    # type the name into the search box
    search_box = scraper.waitUntilFound("input", "id", "desktop_search_field")
    # type the exoplanet name
    scraper.typeBox(search_box, name)
    # search for the exoplanet link
    elem = scraper.find("li", "class", "display_name")
    # try to find the link in the element
    href = scraper.findInHTML(elem, "href")
    # and return the link for this exoplanet
    return "https://exoplanets.nasa.gov/"+href

# fetch all exoplanet links on the page
def fetch_exoplanet_links(scraper):
    ''' Use the NASA Site to return a dictionary of all exoplanet links. '''
    print("Fetching exoplanet links")
    # empty dictionary that stores reference information
    refs = dict()
    # look for how many pages of results there are
    page_total = scraper.waitUntilFound("span", "class", "total_pages").text
    # find a reference to the next page button to click when done
    next_page = scraper.find("a", "rel", "next")
    # and the total number of exoplanets to look for
    total_planets = scraper.waitUntilFound("span", "class", "total_results").text

    # show the current exoplanet index
    def get_start():
        return scraper.waitUntilFound("span", "class", "start_index").text
    sidx = _sidx = get_start()

    # now itterate on each page
    for x in trange(int(page_total)):
        # compile a list of all exoplanets on the page
        results_table = scraper.find("div", "id", "results")
        # fetch a reference to all exoplanets in the table
        for exoplanet in scraper.findAll("ul", "class", "exoplanet", results_table):
            # the link
            link = scraper.findLink(exoplanet)[0]
            # the name is the final part of the link that isn't empty
            name = link.split("/")[-2]
            # ad to our ref dict
            refs[name] = {"link":"https://exoplanets.nasa.gov/"+link}
        # go to the next page
        next_page.click()
        # if we reached the end of the values, stop the loop
        if scraper.waitUntilFound("span", "class", "end_index").text == total_planets:
            continue
        # wait until the start index increases
        while sidx == _sidx:
            wait(0.1)
            _sidx = get_start()
        sidx = _sidx
    print("All exoplanet pages scraped")
    # and return the dict
    return refs

# locate all relevant information of an exoplanet on the page
def exoplanet_info(scraper, link):
    ''' Fetch all the required information for a given exoplanet link page. '''
    info = dict()
    # find the wysiwyd description
    description = scraper.find("p", source=scraper.find("div", "class", "wysiwyg_content")).text
    info["Description"] = description
    # fetch the information grid for this planet
    info_grid = scraper.waitUntilFound("table", "class", "information_grid")
    # fetch all table details
    results = scraper.findAll("tr", "class", "fact_row")
    # look through the table for the details
    for details in results:
        # some fact rows have multiple facts
        facts = scraper.findAll("div", "class", "value", details)
        names = scraper.findAll("div", "class", "title", details)
        # fetch the values, removing empty
        facts = [fact.text for fact in facts if fact.text != ""]
        names = [name.text for name in names if name.text != ""]
        # zip the fact name, and the fact value together
        for name, fact in zip(names, facts):
            # and store them in our dictionary
            info[name.title()] = fact.replace("\n", " ")
    # return the planet information
    return info

# fetch exoplanet images
def fetch_exoplanet_images(scraper, planet_dict, data_location):
    ''' Navigate an exoplanet page and take screenshots of the interactive artists element as images.
        planet_dict: the dictionary of planetary details to be saved, see "generate_details". '''
    # blank image references dictionary
    images = dict()
    # switch to the iframe, with a timeout for loading
    with scraper.loadIframe("exo_pioneer_module", timeout=10) as iframeUrl:
        # store the ifram url in the image references
        images["Link"] = iframeUrl
        # fetch the dropdown section
        planetDropdown = scraper.waitUntilFound("div", "id", "dropUpId")
        # start the image id at zero
        imageId = 0
        # fetch the comparison dropdown
        options, select_option = scraper.waitForSelectbox("class", "dropdownInfo")
        # give it a second to load the image
        wait(1)
        # itterate on the options backwards (Jupiter, Earth, self)
        for option in options[::-1]:
            # select this comparison
            select_option(option)
            # wait for this to load
            wait(1)
            # local filepath for this image
            imageLink = "{}/images/{}.png".format(data_location, imageId)
            # take a screenshot of this option
            scraper.screenshot(imageLink)
            # and fetch the description for this image. (compare, compare to earth, compare to jupiter).
            description = option.replace("COMPARE TO", "COMPARISON WITH") if "TO" in option else planet_dict["Name"]
            # store a reference to this image in the dict
            images[str(imageId)] = {"Path": imageLink,
                                    "Description": description.capitalize(),}
            # increment the image id
            imageId += 1
    # add the images to the dictionary
    planet_dict["images"] = images
    # and return the dictionary
    return planet_dict

# save all the details as an easily accessible pandas dataframe, to be saved externally
def saveToCSV(dfname, thisdata, dataFolderPath):
    # create a dataframe row from a dictionary
    def dict_to_df(data={}, headers=[]):
        # empty output dictionary
        df = {}
        # iterate on headers
        for head in headers:
            # if a valid value is found
            if head in data:
                thisdata = data[head]
                df[head] = [thisdata]
            else:
                # initialize as empty
                df[head] = [""]
        # return the dataframe
        return pd.DataFrame(df)
    # fetch the dataframe extension
    ext = pathlib.Path(dfname).suffix
    # if there isn't one
    if not ext:
        dfname+=".csv"
    # and if it's not csv
    elif ext != ".csv":
        dfname.replace("ext", ".csv")
    # if the file dosen't exist
    if not pathlib.Path(dfname).exists():
        # create the desired headers for each planet
        headers = [# Detail
                   "Name",
                   "Description",
                   "Discovery Date",
                   "Detection Method",
                   # Properties
                   "Mass",
                   "Planet Radius",
                   "Planet Type",
                   # Orbit
                   "Orbital Radius",
                   "Eccentricity",
                   "Orbital Period",
                   # Database details
                   "File",
                   "Uuid",
                   "Link",]
        # create the dataframe object
        df = pd.DataFrame(columns=headers)
    else:
        # fetch from file
        df = pd.read_csv(dfname)
    # fetch the dataframe headers
    headers = df.columns.values.tolist()
    # ensure the file is also added to this planet data
    thisdata["File"] = dataFolderPath+"/"
    # create the dataframe row
    df_row = dict_to_df(thisdata, headers=headers)
    # check if this entry is already there
    entry = df.index[df["Name"] == thisdata["Name"]].tolist()
    if entry:
        # insert new value at old index
        df.loc[entry[0]] = df_row.loc[0]
        # remove any duplicates
        df.drop(entry[1:])
    else:
        # else, append to the end of the dataframe
        df = pd.concat((df, df_row))
    # and save the dataframe
    df.to_csv(dfname, index=False)

# fetch all the details for all the exoplanets
def generate_details(scraper, ref, fileStore="", stale_time=7):
    ''' Convert a dictionary of links into a dictionary of exoplanet information.
        scraper: an instance of the Scraper class to be used to fetch information.
        ref: a dictionary of links to the relevant page.
        fileStore: the directory for which each exoplanet information will be saved to.
        stale_time: the time to consider this file stale, see "Scraper.loadJson" for details. '''
    # fetch a list of references to search
    planets = list(ref.keys())
    # for every reference in the dictionary
    for x in trange(len(planets)):
        # fetch this planet reference
        name = planets[x]
        link = ref[name]["link"]
        # get the folder for this exoplanet
        data_loc = "{}/{}".format(fileStore, name.replace(" ", "_"))
        # check if this exoplanet has information already
        old_details = scraper.loadJSON(data_loc+"/details.json", stale_time)
        # if this exoplanet hasn't previously been searhed
        if not old_details:
            # use the name as an id, generate a uuid from it, and create the dictionary for this planet from that
            thisplanet = {"Id": name, "Uuid": str(uuid.uuid4()), "Link": link, "Name": name,}
            # navigate to the page
            scraper.navigate(link)
            # fetch the details for this planet too
            info = exoplanet_info(scraper, link)
            # and combine the info with this planets details
            thisplanet = {**thisplanet, **info}
        # otherwise, use the previously generated details
        else:
            thisplanet = old_details
        # if we haven't saved images, or there aren't any in the details dictionary
        if ("images" not in thisplanet) or (not scraper.checkForFile(data_loc+"/images/0.png")):
            # navigate to the url if we haven't already had to go there
            if old_details:
                scraper.navigate(link)
            # fetch them
            thisplanet = fetch_exoplanet_images(scraper, thisplanet, data_loc)
        # save to our dataframe
        saveToCSV(scraper.filedir+"/exoplanet_table", thisplanet, data_loc)
        # save the details <<<--- Probably modify this if it ends up being too slow
        scraper.saveJSON(data_loc+"/details.json", thisplanet)
        # wait for a small amount of time

# main program loop
def main():
    ''' Main program loop, Will scrape for exoplanet information. '''
    # Try using it on the initial website!
    # create the scraper instance
    scraper = Scraper()

    # if we have any errors
    try:
        # initialise the scraper storage location
        scraper.localStorage("source/raw_data")

        # navigate to the exoplanet page
        scraper.navigate("https://exoplanets.nasa.gov/discovery/exoplanet-catalog/")

        # expand the exoplanets table to the maximum
        per_page = scraper.waitUntilFound("select", "id", "per_page")
        # fetch the selection box
        options, select_func = scraper.selectbox(per_page)
        # select the max
        select_func(max(options))
        # and click
        per_page.click()
        # wait for it to change
        wait(1)
        # scroll down slightly
        scraper.scroll(0.1)
        
        # search for a locally stored links dictionary
        refs = scraper.loadJSON("exoplanet_links.json", 7)
        # otherwise, fetch manually
        refs = refs if refs else fetch_exoplanet_links(scraper)
        # store the links again
        scraper.saveJSON("exoplanet_links.json", refs)
        
        # generate the details for each planet, and pass in the local storage location
        generate_details(scraper, refs, "exoplanet_details", 7)
    # ensure we close the screaper
    finally:    
        # and close the scraping session
        scraper.close()

# only execute if this is the top level code
if __name__ == "__main__":
    upload = False
    # execute
    try:
        main()
    finally:
    #    upload when completed, or if an error occured because I'm too lazy to select multipl eprograms
        if upload:
            import upload_to_aws
            upload_to_aws.main()