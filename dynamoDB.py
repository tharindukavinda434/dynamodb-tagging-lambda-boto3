import boto3




def lambda_handler(event, context):
  
  
  
  tagged_now = 0
  cant_tag   = 0
  alrdy_tagged =0
  all_db_count = 0
  
  
  regions = ["eu-west-1","eu-west-2","us-east-1","us-east-2"]
  #remove ,"us-east-2" when in LE accounts
  
  tagged_now = 0
  cant_tag   = 0
  alrdy_tagged =0
  all_ebs_count = 0
  
  
  for region in regions:
    db_client = boto3.client('dynamodb',region_name=region)
    paginator = db_client.get_paginator('list_tables')
    response_iterator = paginator.paginate()
    
    for page in response_iterator:
      #print(page)

      table_names = page['TableNames']
      
      #print(table_names)

      
      for table_name in table_names:
        all_db_count += 1
        
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        table__arn = (table.table_arn)
        
        
        response_tags = db_client.list_tags_of_resource(ResourceArn=table__arn)
        #print(response_tags)
        
        flag = 0
        
        try:
          for tag in response_tags['Tags']:
            if (tag['key'] == 'abcd'  ):
              flag =1 
              alrdy_tagged += 1
            
        except Exception as e:
          print(e)
          
          
        try:
          if (flag == 0   ):
            
      
            response = db_client.tag_resource(ResourceArn=table__arn,Tags=[{
              'Key': 'abcd',
              'Value': 'abcd'}])
              
            tagged_now += 1
            
            
            
        except Exception as e:
          print(e)
          cant_tag += 1
          
  print('all dynamoDB  count',all_db_count)
  print('already tagged count' ,alrdy_tagged )
  print('tagged from this attempt',tagged_now)
  print('refused to tag',cant_tag )