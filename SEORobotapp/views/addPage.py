from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import Category, Page, SEOMetadata
from ..forms import KeywordForm
import csv
import os
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import re
import unicodedata 

def addPage(request):
    wordpress_url = "http://192.168.56.1/wordpress/"
    username = "chayma"
    application_password = "wassila1704"
    headers = {
        "Content-Type": "application/json"
    }
    
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['title']
            data = extract_data_from_csv(keyword)
            if data:
                for item in data:
                    print("Processing page title:", item['metaTitle'])
                    
                    response = requests.get(f"{wordpress_url}wp-json/wp/v2/pages?search={item['metaTitle']}", auth=HTTPBasicAuth(username, application_password))
                    
                    if response.status_code == 200:
                        pages = response.json()
                        page_exist = [page for page in pages if page['title']['rendered'].strip().lower() == item['metaTitle'].strip().lower()]
                        # Check if the page already exists
                        if page_exist:
                            print("Page exists, updating...")
                            categoryId = getCategoryIfExist(item['categoryTitle'], wordpress_url+'wp-json/wp/v2', headers, username, application_password)
                            if categoryId is None:
                                categoryId = createCategory(item['categoryTitle'], wordpress_url+'wp-json/wp/v2', headers, username, application_password)
                                
                            page_data = {
                                'title': item['metaTitle'],
                                'content': item['content'],
                                'excerpt': item['metadescription'],
                                'categories': [categoryId],
                                'status': 'publish',
                            }
                            response = requests.put(f"{wordpress_url}wp-json/wp/v2/pages/{page_exist[0]['id']}", headers=headers, json=page_data, auth=HTTPBasicAuth(username, application_password))
                        else:
                            print("Page does not exist, creating...")
                            categoryId = getCategoryIfExist(item['categoryTitle'], wordpress_url+'wp-json/wp/v2', headers, username, application_password)
                            if categoryId is None:
                                categoryId = createCategory(item['categoryTitle'], wordpress_url+'wp-json/wp/v2', headers, username, application_password)
                                
                            page_data = {
                                'title': item['metaTitle'],
                                'content': item['content'],
                                'excerpt': item['metadescription'],
                                'categories': [categoryId],
                                'status': 'publish',
                            }
                            response = requests.post(f"{wordpress_url}wp-json/wp/v2/pages", headers=headers, json=page_data, auth=HTTPBasicAuth(username, application_password))
                        
                        if response.status_code not in [200, 201]:
                            print(f"Failed to create/update page. Status code: {response.status_code}, Response: {response.json()}")
                    else:
                        print(f"Failed to retrieve pages. Status code: {response.status_code}, Response: {response.json()}")
                    # Add to database
                    category, created = Category.objects.get_or_create(categoryTitle=item['categoryTitle'].strip())
                    page, created  = Page.objects.update_or_create(title=item['metaTitle'].strip(),
                        defaults={
                            'content':item['content'].strip(),
                            'url':wordpress_url+getSlug(item['metaTitle']),
                            'idCategory':category
                        }
                    )
                    
                    SEOMetadata.objects.create(
                        meta_key='metaTitle',
                        meta_value=item['metaTitle'].strip(),
                        idPage=page
                    )
                    SEOMetadata.objects.create(
                        meta_key='metaDescription',
                        meta_value=item['metadescription'].strip(),
                        idPage=page
                    )
                
                return redirect('/SEORobot/addPage?success=true')
            else:
                return HttpResponse("The metaTitle is not available in the CSV file.")
    else:
        form = KeywordForm()

    return render(request, 'addPage.html', {'form': form})

def getCategoryIfExist(categoryTitle, wordpress_url, headers, username, application_password):
    response = requests.get(f"{wordpress_url}/categories?search={categoryTitle}", headers=headers, auth=HTTPBasicAuth(username, application_password))
    if response.status_code == 200:
        categories = response.json()
        exact_category = [category for category in categories if category['name'].strip().lower() == categoryTitle.strip().lower()]
        
        if exact_category:
            category_id = exact_category[0]['id']
            print(f"Category exists with ID: {category_id}")
            return category_id
        else:
            print("Category does not exist.")
            return None
    else:
        print(f"Failed to search for categories. Status code: {response.status_code}, Response: {response.json()}")
        return None

def createCategory(categoryTitle, wordpress_url, headers, username, application_password):
    category_data = {'name': categoryTitle}
    response = requests.post(f"{wordpress_url}/categories", headers=headers, json=category_data, auth=HTTPBasicAuth(username, application_password))
    
    if response.status_code == 201:
        category = response.json()
        print(f"Category created with ID: {category['id']}")
        return category['id']
    else:
        print(f"Failed to create category. Status code: {response.status_code}, Response: {response.json()}")
        return None
    

def extract_data_from_csv(keyword):
    csv_file_path = os.path.join(settings.BASE_DIR, 'SEORobotapp', 'data.csv')
    data = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['metaTitle'].strip() == keyword.strip():
                data.append(row)
    return data

def getSlug(title):
    normalized_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('ascii')
    lowercased_title = normalized_title.lower()
    slug = re.sub(r'[^a-z0-9-]+', '-', lowercased_title).strip('-')
    slug = re.sub(r'-+', '-', slug)   
    return slug