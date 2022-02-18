from django.http import JsonResponse
from django.shortcuts import  render
from . models import Test, Query
from datetime import datetime
import secrets



def test(request):
    carNumber = request.GET.get('carNumber')
    fio = request.GET.get('fio')
    number = request.GET.get('number')
    columnar = request.GET.get('columnar')
    carModel = request.GET.get('carModel')
    checkedList = request.GET.get('checkedList')
    
    
    
    
    if checkedList:
        print(checkedList)
        checkedList = checkedList.split(' ')
        ifSuccessfully = True
        selectedAnswers = ''
            
        for i in checkedList:
            if i:
                queryAnswer = i.split(':')[0]
                queryId = i.split(':')[1].split('_')[2]
                correctQueryAnswer = Query.objects.get(pk=queryId).correctAnswer
                selectedAnswers += str(queryId)+':'+str(queryAnswer)+','
                print(selectedAnswers)
                if int(queryAnswer) == int(correctQueryAnswer):
                    continue
                else:
                    ifSuccessfully = False
                    
                    
        token = secrets.token_hex(10)
        Test.objects.create(token=token,fio=fio,number=number,columnar=columnar,carNumber=carNumber,carModel=carModel,successfully=ifSuccessfully,selectedAnswers=selectedAnswers).save()
        newTest = Test.objects.get(token=token)
        return JsonResponse({'id':newTest.token})     
    
    test = []
    querys = Query.objects.all()

    for i in range(len(querys)):
        dictonary = {
            'id': querys[i].pk,
            'count': i+1,
            'query': querys[i].query,
            'answer1': querys[i].answer1,
            'answer2': querys[i].answer2,
        }

        if querys[i].answer3:
            dictonary['answer3'] = querys[i].answer3
        if querys[i].answer4:
            dictonary['answer4'] = querys[i].answer4
        if querys[i].answer5:
            dictonary['answer5'] = querys[i].answer5
        if querys[i].answer6:
            dictonary['answer6'] = querys[i].answer6
        if querys[i].answer7:
            dictonary['answer7'] = querys[i].answer7

        dictonary['explanation'] = querys[i].explanation

        test.append(dictonary)

    length = []
    for i in range(1, len(test)+1):
        length.append(str(i))
    date = datetime.today().strftime('%Y-%m-%d')
    
    

    bigData = {
        'test': test,
        'len': length,
        'listLen':len(length),
        'date': date, 
        }
    return render(request, 'mobiGroup/test.html', bigData)


def finishedTest(request,token):
    passedTets = Test.objects.get(token=token)
    selectedAnswers = passedTets.selectedAnswers
    passed = passedTets.successfully
    carNumber = passedTets.carNumber
    fio = passedTets.fio
    number = passedTets.number
    columnar = passedTets.columnar
    carModel = passedTets.carModel
    date = passedTets.date
    
    selectedAnswersDictonary = {}
    
    selectedAnswers = selectedAnswers.split(',')
    for i in selectedAnswers:
        if i:
            selectedAnswersDictonary[i.split(':')[0]] = i.split(':')[1]
    
    # print(selectedAnswersDictonary)
    
    test = []
    querys = Query.objects.all()
    
    

    for i in range(len(querys)):
        dictonary = {
            'id': querys[i].pk,
            'count': i+1,
            'query': querys[i].query,
            'answer1': querys[i].answer1,
            'answer2': querys[i].answer2,
        }

        if querys[i].answer3:
            dictonary['answer3'] = querys[i].answer3
        if querys[i].answer4:
            dictonary['answer4'] = querys[i].answer4
        if querys[i].answer5:
            dictonary['answer5'] = querys[i].answer5
        if querys[i].answer6:
            dictonary['answer6'] = querys[i].answer6
        if querys[i].answer7:
            dictonary['answer7'] = querys[i].answer7

        dictonary['correctAnswer'] = querys[i].correctAnswer
        x = str(querys[i].pk)
        dictonary['selectedAnswer'] = int(selectedAnswersDictonary[x])
        dictonary['explanation'] = querys[i].explanation

        test.append(dictonary)
    
    
    
    # print(test)
        
    bigData = {        
        'test': test,
        'carNumber':carNumber,
        'fio':fio,
        'number':number,
        'columnar':columnar,
        'carModel':carModel,
        'passed':passed,
        'date':date,
    }
    return render(request, 'mobiGroup/finishedTest.html', bigData)
