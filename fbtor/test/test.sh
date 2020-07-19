#/bin/bash!
echo "--------------------------"
echo "Testing FBoolector methods"
echo "--------------------------"
pytest FBoolectorTest.py -s
echo "--------------------------"
echo "Testing BitVecConv methods"
echo "--------------------------"
pytest BitVecConvertTest.py
