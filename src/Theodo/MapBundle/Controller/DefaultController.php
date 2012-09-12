<?php

namespace Theodo\MapBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class DefaultController extends Controller
{
    public function indexAction()
    {
    	$facebookApi = $this->get('fos_facebook.api');
    	$friends = $facebookApi->api('/me/friends?fields=id,name,location');
    	$friends = $friends['data'];

        return $this->render('TheodoMapBundle:Default:index.html.twig');
    }
}
