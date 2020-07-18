#/bin/bash!
echo "--------------------------"
echo "Testing FBoolector methods"
echo "--------------------------"
pytest test/FBoolectorTest.py -s
echo "--------------------------"
echo "Testing BitVecConv methods"
echo "--------------------------"
pytest test/BitVecConvertTest.py
