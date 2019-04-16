# Products RESTful API
_Shilpi, Kraz, Nate Dogg and MP_

Products Microservice for DevOps and Agile Methodologies Stern MBA Class

This repository will be used to create the Products microservice

[![Build Status](https://travis-ci.org/devopsproducts/products.svg?branch=master)](https://travis-ci.org/devopsproducts/products)

### Installation using Vagrant
The easiest way to use this repo is with Vagrant and VirtualBox. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org)

Download [Vagrant](https://www.vagrantup.com)

Then all you have to do is clone this repo and invoke vagrant:

git clone https://github.com/devopsproducts/products.git
cd orders
vagrant up
vagrant ssh
_CD to /vagrant out of the default SSH directory of home/vagrant_
cd /vagrant

Now you can run 'pytest' to run the tests. Always run test cases before changing any code.


### Testing
#### Manually running the Tests

Run the tests using 'pytest'

'$ pytest'

pytest is configured via the included pytest.ini file to automatically include the flags --with-spec --spec-color so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

pytest is also configured to automatically run the coverage tool and you should see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

$ coverage report -m

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases to get higher code coverage.

It's also a good idea to make sure that your Python code follows the PEP8 standard. flake8 has been included in the requirements.txt file so that you can check if your code is compliant like this:

$ flake8 --count --max-complexity=10 --statistics model,service

I've also include pylint in the requirements. If you use a programmer's editor like Atom.io you can install plug-ins that will use pylint while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.
