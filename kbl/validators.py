def validatePaymentDetails(details):
   
    error = {'status': 'ok', 'msg': ''}
    msg = ''

    
    if not details.get('cardno'):
        return error.update({'msg': msg+'Card number not provided ', 'status': 'bad'})
    
    if not details.get('cvv'):
        return error.update({'msg': msg+'cvv number not provided ', 'status': 'bad'})

    if not details.get('pin'):
        return error.update({'msg': msg+'pin number not provided ', 'status': 'bad'})
        
    if not details.get('expirymonth'):
        return error.update({'msg': msg+'expiry month not provided ', 'status': 'bad'})

    #if not details.get('amount'):
        #return error.update({'msg': msg+'amount not provided ', 'status': 'bad'})
        
    if not details.get('expiryyear'):
        return error.update({'msg': msg+'expiry year not provided ', 'status': 'bad'})

    if not details.get('user_id'):
        return error.update({'msg': msg+'user Id not provided ', 'status': 'bad'})

    if not details.get('policy_number'):
        return error.update({'msg': msg+'Policy number not provided ', 'status': 'bad'})

  
    if not details.get('amount'):
        return error.update({'msg': msg+'amount not provided ', 'status': 'bad'})
        
    
    return error
    
