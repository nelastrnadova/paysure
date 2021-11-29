TODO: SOAP (supposed to accept xml?), swagger, code, tests, readme

REQUIREMENTS: Python3.6+

START: python3 paysure/wsgi.py

EXAMPLE CURL: curl 127.0.0.1:8000/pay -v -X POST -d '{"payment_message_request_xml": "<Body><Transaction><Token>1234567890</Token><MCC>5814</MCC><Amount>250</Amount><Currency>EUR</Currency><Transaction_Time>2021-10-21T09:45:12,332+0000</Transaction_Time><Merchant><Name>Royal London Fastfoodtruck</Name><Merchant_City>London</Merchant_City><Location><Lat>51.509865</Lat><Lon>-0.118092</Lon></Location></Merchant></Transaction></Body>"}'