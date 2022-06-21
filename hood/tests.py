from django.test import TestCase
from .models import *

# Create your tests here.

class NeighborHoodTestClass(TestCase):
  '''
  Test class that defines test cases for the model behaviours.

  Args:
      unittest.TestCase: TestCase class that helps in creating test cases
  '''

  def setUp(self):
      '''
      Set up method to run before each test cases.
      It defines instructions that will be executed before each test method.
      '''

      self.new_hood = NeighbourHood(name='Hill View Estate', location="Nairobi", description='Beatiful Estate', emergency= '0712345678', police_number='0712345678', image='hood-images/img1.jpg')

  # FIRST TEST
  def test_instance(self):
      '''
      test_instance test case to test if the object is initialized properly
      '''
      self.assertTrue(isinstance(self.new_hood,NeighbourHood))

  # SECOND TEST
  def test_save_neighborhood(self):
      '''
      test_save_neighborhood test case to test if the object is being created and saved correctly
      '''
      self.new_hood.create_neighborhood()
      self.assertTrue(len(NeighbourHood.objects.all()) > 0)

  # THIRD TEST
  def test_update_neighborhood(self):
      '''
      test_update_neighborhood test case to test if the object is being updated correctly
      '''
      self.new_hood.create_neighborhood()
      self.new_hood.name = "New Hill View Estate"
      self.assertTrue(self.new_hood.name == "New Hill View Estate")

  # FOURTH TEST
  def test_del_neighborhood(self):
      '''
      test_del_neighborhood test case to test if the object is being deleted successfully
      '''
      self.new_hood.create_neighborhood()
      self.new_hood.delete_neighborhood()
      self.assertTrue(len(NeighbourHood.objects.all()) == 0)


class ProfileTestClass(TestCase):
  '''
  Test class that defines test cases for the model behaviours.
  Args:
      unittest.TestCase: TestCase class that helps in creating test cases
  '''

  def setUp(self):
      '''
      Set up method to run before each test cases.
      It defines instructions that will be executed before each test method.
      '''
      #Create and save a User
      self.user = User.objects.create(username='sha')

      self.new_hood = NeighbourHood(name='Hill View Estate', location="Nairobi", description='Beatiful Estate', emergency= '0712345678', police_number='0712345678', image='hood-images/img1.jpg')

      self.new_profile = Profile(user=self.user, profile_image='profile-images/img1.jpg', bio='This is my bio', location="Nairobi", neighborhood=self.new_hood) 

  # FIRST TEST
  def test_instance(self):
      '''
      test_instance test case to test if the object is initialized properly
      '''
      self.assertTrue(isinstance(self.new_profile,Profile))


class BusinessTestClass(TestCase):
  '''
  Test class that defines test cases for the model behaviours.
  Args:
      unittest.TestCase: TestCase class that helps in creating test cases
  '''

  def setUp(self):
      '''
      Set up method to run before each test cases.
      It defines instructions that will be executed before each test method.
      '''
      # Create and save a User
      self.user = User.objects.create(username='sha')

      # Create and save a Hood
      self.new_hood = NeighbourHood(name='Hill View Estate', location="Nairobi", description='Beatiful Estate', emergency= '0712345678', police_number='0712345678', image='hood-images/img1.jpg')

      self.new_business = Business(name="Business Name", email="business@gmail.com", description="Bisiness Description", business_image='hood-images/img1.jpg', neighbourhood=self.new_hood, user=self.user)

  # FIRST TEST
  def test_instance(self):
      '''
      test_instance test case to test if the object is initialized properly
      '''
      self.assertTrue(isinstance(self.new_business,Business))

  # SECOND TEST
  def test_save_business(self):
      '''
      test_save_business test case to test if the object is being saved correctly
      '''
      self.new_business.save_business()
      self.assertTrue(len(Business.objects.all()) > 0)

  # THIRD TEST
  def test_update_business(self):
      '''
      test_update_business test case to test if the object is being updated correctly
      '''
      self.new_business.save_business()
      self.new_business.name = 'Barber Shop'
      self.assertTrue(self.new_business.name  == 'Barber Shop' )

  # FOURTH TEST
  def test_delete_business(self):
      '''
      test_delete_dusiness test case to test if the object is being deleted correctly
      '''
      self.new_business.save_business()
      self.new_business.delete_business()
      self.assertTrue(len(Business.objects.all()) == 0)

  # FIFTH TEST
  def test_search_business(self):
      '''
      test_search_business test case to test if the objects are being retrieved correctly
      '''
      self.new_business.save_business()
      self.assertTrue(len(Business.search_business('Business Name')) > 0)