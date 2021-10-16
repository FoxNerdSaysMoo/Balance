import json


periodic_table = json.load(open("elements.json"))
names = {
    v["symbol"]: i for i, v in enumerate(periodic_table)
}

chemical = input("Reactants (ex. Zn Na 3Cl 2H): ")
charges = input("Charges of reactants (ex. 2 1 -1 1): ")

chem = []

for e, charge in zip(chemical.split(" "), charges.split()):
    count = 1
    elem = e
    if e[0].isdigit():
        c = ""
        for char in e:
            if char.isdigit():
                c += char
                elem = elem.replace(char, "", 1)
        count = int(c)
    element = names[elem]
    for i in range(count):
        chem.append(
            (element+1, int(charge))
        )

result = []

failed = False
c = 0

while not failed:
    charge = None

    result.append(tuple())

    while charge != 0:
        alive = False
        for elem in chem:
            alt = elem[1] * (charge if charge else -elem[1]) < 0
            if alt:
                alive = True
                if charge is not None:
                    charge += elem[1]
                else:
                    charge = elem[1]
                result[c] += (elem,)
                chem.remove(elem)
            if charge == 0:
                break
        if not alive:
            failed = True
            chem += result[c]
            del result[c]
            break

    c += 1

for i in chem:
    bond = periodic_table[i[0]-1]["bondingType"]
    if bond not in ["atomic", "diatomic"]:
        continue
    if bond == "diatomic":
        if chem.count(i) > 1:
            result.append((i,)*2)
    else:
        result.append((i,))

print("Creates")

for compound in set(result):
    for x in [x for x in set(compound) if x]:
        sub = compound.count(x)
        print(
            periodic_table[x[0]-1]["symbol"],
            sub if sub > 1 else "",
            sep="",
            end=""
        )
    print()

