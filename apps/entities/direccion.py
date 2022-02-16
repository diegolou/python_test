class DIRECCION:
  uid = ''
  address = ''
  adnumber = ''
  city = ''
  state = ''
  country = ''
  details = ''
  Formattedaddress = ''
  Latitude = ''
  Longitude = ''
  zipcode = ''
  
  def __init__(self, uid = '', address = '', adnumber = '', city = '', state = '', country = '', details = '', Formattedaddress = '', Latitude = '', Longitude = '', zipcode = ''):
    self.address = address
    self.uid = uid
    self.adnumber = adnumber
    self.city = city
    self.state = state
    self.country = country
    self.details = details
    self.Formattedaddress = Formattedaddress
    self.Latitude = Latitude
    self.Longitude = Longitude
    self.zipcode = zipcode
  
