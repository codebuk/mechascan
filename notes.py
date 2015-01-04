 #'sdram'      
    #capture image
    #gp.check_result(gp.gp_camera_trigger_capture(camera, context))
print (gp.gp_camera_wait_for_event (camera, 2000 , context))

  #set_config ( camera, context, 'eosremoterelease',  'Release Full' )
    #time.sleep(5)
      #time.sleep(2)
    #set_config ( camera, context, 'eosremoterelease',  'None' )
    
    #OK, etype, edata = gp.gp_camera_wait_for_event (camera, 2000 , context)
    #if (etype == gp.GP_EVENT_TIMEOUT):
    #    print ("dfegerge")
    #print (etype)
    #print (edata)
       #print (gp.gp_camera_wait_for_event (camera, 2000 , context))
    #gp.check_result(gp.gp_file_save(camera_file, "eeee"))
