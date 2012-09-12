<?php

namespace Theodo\MapBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class DefaultController extends Controller
{
    public function indexAction()
    {
    	$friendManager = $this->get('theodo_map.friend_manager');
    	$facebookApi = $friendManager->getFacebookApi();
    	$user = $friendManager->getMe();
    	$friends = $friendManager->getFriends();


        return $this->render('TheodoMapBundle:Default:index.html.twig', array(
        	'user' => $user,
        	// 'user' => array('first_name'=> 'jonathan'),
        ));
    }
}
