from apps.department.models import Department, Size


Size.objects.all().delete()

d1s = [36, 38, 40, 42, 44, 46, 48, 50, 52, 54]
d2s = [36, 38, 40, 42, 44, 46, 48, 50, 52, 54, "NA"]
d4s = [28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
d3s = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16]
d1 = [
    "SHORT KURTA",
    "SHIRT",
    "T SHIRT",
    "BLAZER",
    "WOOLEN",
    "WAIST COAT SUIT",
    "COTI",
    "KURTA SHRUG",
    "SEMI INDO",
    "KURTA COTI",
    "PATHANI",
    "KURTA PAJAMA",
    "SHERWANI",
    "DARK INDO",
    "JODHPURI",
    "5P SUIT",
    "2P SUIT",
]
d2 = ["ACCESSORIES"]
d3 = ["KIDS"]
d4 = ["JEANS", "TROUSER"]


def doit(d, ds):
    for department_name in d:
        print(department_name)
        department = Department.objects.get(department_name=department_name)
        for i in ds:
            Size.objects.get_or_create(department=department, size_value=i)

doit(d1, d1s)
doit(d2, d2s)
doit(d3, d3s)
doit(d4, d4s)
