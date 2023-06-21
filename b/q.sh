counter=1
while IFS= read -r name; do
    name=$(echo "$name" | xargs)
    
    curl --location --request POST "http://127.0.0.1:8000/${counter}" -H 'Content-Type: application/json' -d '{"name":"'${name}'"}'
    curl --location --request GET "http://127.0.0.1:8000/${counter}" >> ./mypath/response.txt
    
    counter=$((counter+1))

done < ./queries.txt

echo "#########"
cat ./mypath/response.txt