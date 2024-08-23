# Extract lot dimensions
            # lot_dimensions_elements = soup.find_all('div', class_='listing-main-characteristics__item--lot-dimensions')
            lot_dimensions = soup.find('span', class_='listing-main-characteristics__number listing-main-characteristics__number--dimensions')
            if lot_dimensions :
                property_details['Lot Dimensions'] = lot_dimensions.text.strip()

            # Extract number of bedrooms
            # bedroom_elements = soup.find_all('div', class_='listing-main-characteristics__item')
            bedroom_counts = soup.find('span', class_='listing-main-characteristics__number')
            if bedroom_counts :
                print(bedroom_counts)
                property_details['Bedrooms'] = int(bedroom_counts.text.strip())

            # Extract number of bathrooms
            # bathroom_elements = soup.find_all('div', class_='listing-main-characteristics__item--bathrooms')
            bathroom_counts = soup.find('span', class_='listing-main-characteristics__number')
            if bathroom_counts :
                property_details['Bathrooms'] = int(bathroom_counts.text.strip())

            # Extract number of levels
            # level_elements = soup.find_all('div', class_='listing-main-characteristics__item')
            level_counts = soup.find('span', class_='listing-main-characteristics__number')
            if level_counts :
                property_details['Levels'] = int(level_counts.text.strip())

            # Extract living space area
            # living_space_elements = soup.find_all('div', class_='listing-main-characteristics__item--living-space-area')
            living_space_area = soup.find('span', class_='listing-main-characteristics__number listing-main-characteristics__number--dimensions')
            if living_space_area :
                property_details['Living Space Area'] = living_space_area.text.strip()