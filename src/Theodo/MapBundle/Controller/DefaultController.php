<?php

namespace Theodo\MapBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Response;

class DefaultController extends Controller
{
    public function indexAction()
    {
    	$friendsLocationManager = $this->get('theodo_map.friends_location_manager');
    	$user = $friendsLocationManager->getMe();

        return $this->render('TheodoMapBundle:Default:index.html.twig', array(
        	'user' => $user,
        ));
    }
}
