from webbot import Browser
import re
import pandas as pd

# Get the quantities of the item.
def cQuantities(f):
    itemLocations = [];
    quantities = [];

    for match in re.finditer("availability-status-indicator__text", f):
        itemLocations.append((match.end()) + 2);
        
    for i in range(len(itemLocations)):
        if f[itemLocations[i]] == 'I':
            itemLocations[i] += 67;
            quantities.append(str(f[itemLocations[i]]));
        
            j = 1;
            while f[itemLocations[i] + j].isdigit():
                quantities[i] += str(f[itemLocations[i] + j]);
                j += 1;
            
        else:
            quantities.append('0');
        
    return quantities;

# Get the prices of the item.
def cPrices(f):
    itemLocations = [];
    prices = [];
    
    for match in re.finditer("table__cell-price  table__cell-price", f):
        itemLocations.append(match.end());
        
    for i in range(len(itemLocations)):
        j = 50;
        while not f[itemLocations[i] + j].isdigit():
            j += 1;
        
        itemLocations[i] += j;
        
        prices.append(f[itemLocations[i]]);
        
        j = 1;
        while f[itemLocations[i] + j].isdigit():
            prices[i] += str(f[itemLocations[i] + j]);
            j += 1;
        
        prices[i] += '.';
        
        prices[i] += str(f[itemLocations[i] + j + 85]);
        prices[i] += str(f[itemLocations[i] + j + 86]);
    
    priceList = [];
    
    for i in prices:
        try:
            priceList.append(float(i));
        except:
            priceList.append(float(i[:2]));
    
    return priceList;

# Get the locations of the item.
def cLocations(f):
    itemLocations = [];
    location1 = [];
    location2 = [];
    location3 = [];
    
    for match in re.finditer("address-location-name", f):
        itemLocations.append(match.end() + 2);
        
    for i in range(len(itemLocations)):
        location1.append(str(f[itemLocations[i]]));
        
        j = 1;
        while f[itemLocations[i] + j] != "<":
            location1[i] += str(f[itemLocations[i] + j]);
            j += 1;
            
        itemLocations[i] += j + 37;

    # itemLocations carries over from location1.
    for i in range(len(itemLocations)):
        location2.append(str(f[itemLocations[i]])[1:]);
        
        j = 1;
        while f[itemLocations[i] + j] != "<":
            location2[i] += str(f[itemLocations[i] + j]);
            j += 1;
        
        itemLocations[i] += j + 6;

    # itemLocations carries over from location2.    
    for i in range(len(itemLocations)):
        location3.append(str(f[itemLocations[i]]));
        
        j = 1;
        while f[itemLocations[i] + j] != "<":
            location3[i] += str(f[itemLocations[i] + j]);
            j += 1;
        
        location3[i] = location3[i][:-1];
            
    return location1, location2, location3;

# Get the information for an item in all stores near a zip code and print it.
def main():
    web = Browser();
    web.go_to("https://brickseek.com/walmart-inventory-checker/?sku=108208974");

    web.type("30022", into = "Zip Code");
    web.press(web.Key.ENTER);

    f = web.get_page_source();

    quantities = cQuantities(f);
    
    prices = cPrices(f);
    
    location1, location2, location3 = cLocations(f);
    
    print(pd.DataFrame({"quantity":quantities, "price":prices, "address 1":location1, "address 2":location2, "address 3":location3}));
    
if (__name__ == "__main__"):
    main();
