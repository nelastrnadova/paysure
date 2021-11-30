TODO: 
- SOAP (supposed to accept xml?)
- WSDL,
- remove todos
- database
- initial db loading from included csv
- write tests (and actually testing the code itself)
- readme
- logs, docs, dockerfile etc..

REQUIREMENTS: 
- Python3.6+

START: 
- cd paysure
- python3 wsgi.py

EXAMPLE CURL: 
- `curl 127.0.0.1:8000/pay -v -X POST -d '{"payment_message_request_xml": "<Body><Transaction><Token>1234567890</Token><MCC>5814</MCC><Amount>250</Amount><Currency>EUR</Currency><Transaction_Time>2021-10-21T09:45:12,332+0000</Transaction_Time><Merchant><Name>Royal London Fastfoodtruck</Name><Merchant_City>London</Merchant_City><Location><Lat>51.509865</Lat><Lon>-0.118092</Lon></Location></Merchant></Transaction></Body>"}'`