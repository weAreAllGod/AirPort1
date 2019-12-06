s="We Are Happy"
result=""
for i in s:
    if i==" ":
        result+="%20"
    else:
        result+=i
print(result)