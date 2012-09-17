<?php

namespace Theodo\MapBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;

class ApiController extends Controller
{
    public function friendsAction()
    {
        $friendsLocationManager = $this->get('theodo_map.friends_location_manager');
        $friends = $friendsLocationManager->getFriends();

        $response = new Response(json_encode($friends));

        return $response;
    }
}
