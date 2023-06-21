counter=1
while IFS= read -r name; do
    name=$(echo "$name" | xargs)
    
    echo "#########"
    echo $counter
    curl --location --request POST "http://127.0.0.1:8000/dishes" -H 'Content-Type: application/json' -d '{"name":"'${name}'"}'
    curl --location --request GET "http://127.0.0.1:8000/dishes/${counter}" >> mypath/response
    
    counter=$((counter+1))

done < queries.txt

echo "#########"
cat mypath/response