# Written by Vishaal Vageshwari

def getIndexRangeInput(message):
    indexRangeArr = []
    confirmed = False

    while not confirmed:
        indexRangeStr = input("Select index range (e.g message 1: 0 2 --> 'Lpa'): ")
        indexRangeStrArr = indexRangeStr.split(' ')
        
        if len(indexRangeStrArr) != 2:
            print("Usage: <first index> <second index>")
            continue
        elif int(indexRangeStrArr[0]) < 0 or int(indexRangeStrArr[0]) > len(message) - 1:
            print("First index out of range. Try again.")
            continue
        elif int(indexRangeStrArr[1]) < 0 or int(indexRangeStrArr[1]) > len(message) - 1:
            print("Second index out of range. Try again.")
            continue
        elif int(indexRangeStrArr[0]) > int(indexRangeStrArr[1]):
            print("Second index must be greater than or equal to the first index. Try again.")
            continue
        else:
            indexRangeArr.append(int(indexRangeStrArr[0]))
            indexRangeArr.append(int(indexRangeStrArr[1]))

            print("This is the substring you want to guess: '{0}'".format(message[indexRangeArr[0]:(indexRangeArr[1] + 1)]))

            confirm = str(input("Is this right [y/n]: "))
            
            if confirm == "y":
                confirmed = True

    return indexRangeArr

def getCribInput(validCribLength):
    crib = ""
    validInput = False

    while not validInput:
        print(f"A valid crib for you is {validCribLength} characters long")
        
        crib = str(input("Enter a valid crib: "))

        if len(crib) != validCribLength:
            print("Sorry the crib length {0} but it should be {1}. Try again.".format(len(crib), validCribLength))
        else:
            validInput = True

    return crib

def getOtpGuess(message, crib, bound1, bound2):
    otpGuess = ""
    message = message.lower()
    crib = crib.lower()
    targetAscii = [ord(c) for c in message[bound1:bound2 + 1]]
    cribAscii = [ord(c) for c in crib]

    if len(targetAscii) != len(cribAscii):
        print("Somethings gone wrong crib and target are not of the same length")
        return otpGuess

    for i in range(0, len(targetAscii)):
        ta = targetAscii[i] - 96
        ca = cribAscii[i] - 96
        otpCharAscii = (ta - ca) % 26

        if otpCharAscii == 0:
            otpCharAscii += 26

        otpCharAscii += 96
        otpGuess += chr(otpCharAscii)

    return otpGuess


def decryptOtp(message, otpGuess, bound1, bound2):
    decryptedOtp = ""
    message = message.lower()
    otpGuess = otpGuess.lower()
    messageAscii = [ord(c) for c in message]
    otpGuessAscii = [ord(c) for c in otpGuess]

    for i in range(0, len(otpGuess)):
        messageIndex = i + bound1
        ma = messageAscii[messageIndex] - 96
        oa = otpGuessAscii[i] - 96
        decryptCharAscii = (ma - oa) % 26

        if decryptCharAscii == 0:
            decryptCharAscii += 26

        decryptCharAscii += 96
        messageAscii[messageIndex] = decryptCharAscii
    
    for num in messageAscii:
        decryptedOtp += chr(num)

    return decryptedOtp

def main():
    messages = {
        1: "LpaGbbfctNiPvwdbjnPuqolhhtygWhEuafjlirfPxxl",
        2: "WdafvnbcDymxeeulWOtpoofnilwngLhblUfecvqAxs",
        3: "UijMltDjeumxUnbiKstvdrVhcoDasUlrvDypegublg",
        4: "LpaAlrhGmjikgjdmLlcsnnYmIsoPcglaGtKeQcemiu",
        5: "LpaDohqcOzVbglebjPdTnoTzbyRbuwGftflTliPiqp"
    }

    for k, v in messages.items():
        length = len(v)
        print(f"{k}: {v} [{length}]")

    chosenMessage = messages[int(input("Encrypted message to guess from: "))]
    indexRangeArr = getIndexRangeInput(chosenMessage)
    validCribLength = (indexRangeArr[1] - indexRangeArr[0]) + 1
    crib = getCribInput(validCribLength)
    otpGuess = getOtpGuess(chosenMessage, crib, indexRangeArr[0], indexRangeArr[1])

    if not otpGuess:
        return

    print(f"Crib entered = '{crib}'")
    print(f"OTP guess produced = '{otpGuess}'")
    print("\n\n")
    print(f"Using OTP '{otpGuess}' to decrpyt:")

    for k, v in messages.items():
        print(f'Orginal {k}: {v}')

    print("\n\n")

    for k, v in messages.items():
        partOfOtp = otpGuess
        bound1 = indexRangeArr[0]
        bound2 = indexRangeArr[1]

        if bound1 + 1 > len(v):
            print(f"Guessed {k}: {v.lower()}")
            break
        elif bound2 + 1 > len(v):
            bound2 = len(v) - 1
            till = (bound2 - bound1) + 1
            partOfOtp = partOfOtp[:till]

        decryptedOtp = decryptOtp(v, partOfOtp, bound1, bound2)
        print(f"Guessed {k}: {decryptedOtp}")

if __name__ == "__main__":
    main()