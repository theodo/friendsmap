<?php

namespace Theodo\MapBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;

class ApiController extends Controller
{
    public function friendsAction()
    {
        $friendManager = $this->get('theodo_map.friend_manager');
        $friends = $friendManager->getFriends();

        $response = new Response(json_encode($friends));  
        return $response;  
    }
}
