counter=1
while IFS= read -r name; do
    name=$(echo "$name" | xargs)
    
    #curl --location --request POST "http://127.0.0.1:8000/dishes" -H 'Content-Type: application/json' -d '{"name":"'${name}'"}'
    curl --location --request POST "http://127.0.0.1:8000/dishes" -H 'Content-Type: application/json' -d "{\"name\":\"${name}\"}"

    response=$(curl --location --request GET "http://127.0.0.1:8000/dishes/${counter}")
    
    cal=$(echo "$response" | jq -r '.cal')
    sodium=$(echo "$response" | jq -r '.sodium')
    sugar=$(echo "$response" | jq -r '.sugar')

    echo "${name} contains (${cal}) calories, (${sodium}) mgs of sodium and (${sugar}) grams of sugar" >> mypath/response
    
    counter=$((counter+1))

done < queries.txt

cat mypath/response