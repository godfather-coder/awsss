import json
import time

from django.db import transaction

from .ImageConverter import ImageConverter
from .PaidServiceAPI import PaidServiceAPI
from .RealEstateDraftCreator import RealEstateClient
from .deleteDraft import DeleteDraft
from .getOrderSs import WebDataExtractor
from .ssImage import ImageUploader
from .utiles import Utiles
from .jwt import JWTExtractor

def UploadOnSS(ids, token, user):
    result = []
    successful_uploads = 0
    failed_uploads = []
    for singleId in ids:
        try:
            delte = DeleteDraft(token)
            delte.delete_draft()
            url = "https://home.ss.ge/ka/udzravi-qoneba/" + singleId
            extractor = WebDataExtractor(url)
            jwtextractor = JWTExtractor()

            userInfo = jwtextractor.extract_payload("eyJhbGciOiJSUzI1NiIsImtpZCI6IkEzMTIxOUJCRUNCNTkyNkNEOTEzMzJDMkIwNTMzMEJERENFNkRBODJSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im94SVp1LXkxa216WkV6TENzRk13dmR6bTJvSSJ9.eyJuYmYiOjE3MjQ0NDQ5NDEsImV4cCI6MTcyNDQ0ODU0MSwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LnNzLmdlIiwiYXVkIjpbInVzZXJfcmVnaXN0cmF0aW9uIiwiSm9iYXJpYUFQSSIsInBhaWRfc2VydmljZXMiLCJ3ZWJfYXBpZ2F0ZXdheSIsInJlYWxfZXN0YXRlIiwic3RhdGlzdGljcyIsImZpbGVzIiwiaG91c2VfYXBpIl0sImNsaWVudF9pZCI6InNzd2ViIiwic3ViIjoiYjRmYTY0YTYtMzAwNC00YTdkLWFmMjctZGU3YmNjOWE4N2E4IiwiYXV0aF90aW1lIjoxNzI0Mzk5OTY3LCJpZHAiOiJsb2NhbCIsInByZWZlcnJlZF91c2VybmFtZSI6IndwYXB1bmExOTk1QGdtYWlsLmNvbSIsIklzUHJlbWl1bSI6IkZhbHNlIiwiU2hvd0FkcyI6IlRydWUiLCJlbWFpbCI6IndwYXB1bmExOTk1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjoiVHJ1ZSIsInBob25lX251bWJlciI6IjU5ODc1NzU5NiIsInBob25lX251bWJlcl92ZXJpZmllZCI6IlRydWUiLCJVc2VyRW50aXR5VHlwZSI6IkluZGl2aWR1YWwiLCJQSU4iOiI5NTY0NDAwIiwibmFtZSI6IuGDnuGDkOGDnuGDo-GDnOGDkCIsIlJvbGVzIjoiIiwiaWF0IjoxNzI0NDQ0OTQxLCJzY29wZSI6WyJmaWxlcyIsImhvdXNlX2FwaSIsIm9wZW5pZCIsInBhaWRfc2VydmljZXMiLCJwcm9maWxlIiwicmVhbF9lc3RhdGUiLCJzdGF0aXN0aWNzIiwidXNlcl9yZWdpc3RyYXRpb24iLCJ3ZWJfYXBpZ2F0ZXdheSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJvdHAiXX0.FJsFZkxDq4hG9PD2SMAYTWE9Z2aTMZUdNzzLZY00Qtu28bFrJS6my09rpjsZakt7YfG0dF4EgTwDENrwB3IEBBiuWUfI8dbJ398OCLgeaYEmeF9POKDvicnbDdIy9b-huYbFfK2dtfyOSZ-Epvw42rxtSTo_48wozTRDNSMX6ZxY4WveuK7Kgh2cUFyyauE40x_UuHqcpk25JHN3jw9F1OXpbqgUbg4Yhsv7xgQ7RUysDxIqFy_ciIdElzFClRvvK5_NSTmv4jSDCCZzFYgEEg0-YhVF_ObUjh4TmIThXTXDNll6m0HVQaMPm-_gzlSyHrWsTLDWw5-_oZrtdLSIcA")

            api_client = RealEstateClient(token)
            extractor.fetch_html()
            utiles = Utiles()
            application_data = extractor.extract_application_data('__NEXT_DATA__')
            json.dumps(application_data, indent=4, ensure_ascii=False)
            print("teste")
            application_data1 = {
                "application": {
                    "userType": "Individual",
                    "realEstateTypeId": application_data.get('realEstateTypeId', False),
                    "realEstateDealTypeId": application_data.get('realEstateDealTypeId', False),
                    "cityId": application_data.get('address', {}).get('cityId', False),
                    "currencyId": application_data.get('price', {}).get('currencyType', False),
                    "showSiteCurrencyId": application_data.get('price', {}).get('currencyType', False),
                    "priceType": 1,
                    "phoneNumbers": [
                        {
                            "hasViber": False,
                            "hasWhatsapp": False,
                            "isApproved": False,
                            "isMain": True,
                            "phoneNumber": userInfo['phone_number']
                        }
                    ],
                    "subdistrictId": application_data.get('address', {}).get('subdistrictId', False),
                    "streetId": application_data.get('address', {}).get('streetId', False),
                    "bedrooms": application_data.get('bedrooms', False),
                    "price": application_data.get('price', {}).get('priceGeo', False),
                    "priceUsd": application_data.get('price', {}).get('priceUsd', False),
                    "unitPrice": application_data.get('price', {}).get('unitPriceGeo', False),
                    "unitPriceUsd": application_data.get('price', {}).get('unitPriceUsd', False),
                    "balconyLoggia": utiles.getBallId(application_data.get('balcony_Loggia', "არ აქვს")),
                    "status": application_data.get('realEstateStatusId', False),
                    "viewOnTheYard": application_data.get('viewOnYard', False),
                    "balcony": application_data.get('balcony', False),
                    "garage": application_data.get('garage', False),
                    "naturalGas": application_data.get('naturalGas', False),
                    "storage": application_data.get('storage', False),

                    'cadastralCode': application_data.get('cadastralCode', False),
                    "heating": application_data.get('heating', False),
                    "basement": application_data.get('basement', False),
                    "elevator": application_data.get('elevator', False),
                    "lastFloor": application_data.get('lastFloor', False),
                    "descriptionGe": application_data.get('description', {}).get('ka', False),
                    "descriptionEn": application_data.get('description', {}).get('en', False),
                    "descriptionRu": application_data.get('description', {}).get('ru', False),
                    "cableTelevision": application_data.get('cableTelevision', False),
                    "drinkingWater": application_data.get('drinkingWater', False),
                    "electricity": application_data.get('electricity', False),
                    "fridge": application_data.get("fridge", False),
                    "furniture": application_data.get("furniture", False),
                    "glazedWindows": application_data.get("glazedWindows", False),
                    "hotWater": application_data.get("hotWater", False),
                    "internet": application_data.get("internet", False),
                    "ironDoor": application_data.get('ironDoor', False),
                    "securityAlarm": application_data.get('securityAlarm', False),
                    "sewage": application_data.get('sewage', False),
                    "telephone": application_data.get('telephone', False),
                    "tv": application_data.get('tv', False),
                    "washingMachine": application_data.get('washingMachine', False),
                    "water": application_data.get('water', False),
                    "wiFi": application_data.get('wiFi', False),
                    "withPool": application_data.get('withPool', False),
                    "viewOnTheStreet": application_data.get('viewOnStreet', False),
                    "comfortable": application_data.get('comfortable', False),
                    "light": application_data.get('light', False),
                    "airConditioning": application_data.get('airConditioning', False),
                    "commercialRealEstateType": application_data.get('commercialType', False),
                    "floorType": application_data.get('floorType', False),
                    "kitchenArea": application_data.get('kitchenArea', False),
                    "contactPerson": userInfo['name'],
                    "hasRemoteViewing": application_data.get('hasRemoteViewing', False),
                    "isForUkraine": False,
                    "isPetFriendly": False,
                    "streetNumber": str(application_data.get('address', {}).get('streetId', '')),
                },
            }
            if utiles.getProjectId(application_data.get('project')):
                application_data1['application']['project'] = utiles.getProjectId(
                    application_data.get('project', False))

            if utiles.getStateId(application_data.get('state')):
                application_data1['application']['state'] = utiles.getStateId(application_data.get('state'))

            if application_data.get('rooms') is not None:
                application_data1['application']['rooms'] = application_data.get('rooms', 0)

            if application_data.get('floor') != "":
                application_data1['application']['floor'] = int(application_data.get('floor', 0))

            if application_data.get('floors') is not None:
                application_data1['application']['floors'] = int(application_data.get('floors', 0))

            if utiles.getToiletId(application_data.get('toilet')):
                application_data1['application']['toilet'] = utiles.getToiletId(application_data.get('toilet'))

            if utiles.getLivesWithId(application_data.get('houseWillHaveToLive')):
                application_data1['application']['willLiveInHouse'] = utiles.getLivesWithId(
                    application_data.get('houseWillHaveToLive'))

            if application_data.get('totalArea') != "":
                try:
                    application_data1['application']['totalArea'] = int(application_data.get('totalArea', 0))
                except:
                    application_data1['application']['totalArea'] = application_data.get('totalArea', 0)



            applicationIdDr = api_client.create_draft(application_data1['application'])

            urls = []

            for img in application_data['appImages']:
                urls.append(img['fileName'])
            imagebase = ImageConverter(urls)
            image_urls = imagebase.get_base64_images()
            imaUpl = ImageUploader(applicationIdDr['applicationId'], token)
            upl_imag_arr = []
            for base_64 in image_urls:
                res = imaUpl.upload_image(base_64)
                upl_imag_arr.append({
                    "applicationImageId": res["imageId"],
                    "fileName": res["fileName"],
                    "isMain": False,
                    "is360": False,
                    "orderNo": 0,
                    "imageRotation": 0
                })
            application_data1['paidServices'] = {
                "isCreate": True,
                "items": [
                    {
                        "applicationId": applicationIdDr['applicationId'],
                        "rubric": "RealEstate",
                        "realEstateDealTypeId": 4,
                        "cityId": 95,
                        "paidServices": []
                    }
                ]
            }
            application_data1['application']["images"] = upl_imag_arr
            application_data1['application']['realEstateApplicationId'] = applicationIdDr['applicationId']
            api = PaidServiceAPI(token)


            response = api.create_application(application_data1)
            print(application_data1)
            if response == 200:
                result.append("განცხადება " + singleId + " წარმატებით დაიდო")
                successful_uploads += 1
            else:
                result.append("შეცდომა აიდი " + singleId + "-ის დადებისას")
                failed_uploads.append(singleId)
        except Exception as e:
            result.append("შეცდომა აიდი " + singleId + "-ის დადებისას")

            failed_uploads.append(singleId)
    with transaction.atomic():
        user.total_listings += successful_uploads
        user.failed_listings_ss.extend(failed_uploads)
        user.save()

    return result
