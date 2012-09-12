<?php

namespace Theodo\MapBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class DefaultController extends Controller
{
    public function indexAction()
    {
    	$facebookApi = $this->get('fos_facebook.api');
    	$user = $facebookApi->api('/me');
    	$friends = $facebookApi->api('/me/friends?fields=id,name,location');
    	$friends = $friends['data'];


        return $this->render('TheodoMapBundle:Default:index.html.twig', array(
        	'user' => $user,
        ));
    }
}
