<?php

namespace Theodo\MapBundle\Manager;

use \Theodo\MapBundle\Document\Location;

class FriendsLocationManager
{

    protected $facebookApi;
    protected $dm;

    /**
     * @param BaseFacebook $facebookApi
     * @param DocumentManager $doctrineMongodb
     * @author jonathanb
     * @since 2012-09-14
     */
    public function __construct($facebookApi, $doctrineMongodb)
    {
        $this->facebookApi = $facebookApi;
        $this->dm = $doctrineMongodb->getManager();
    }

    /**
     * @return BaseFacebook
     * @author jonathanb
     * @since 2012-09-14
     */
    public function getFacebookApi()
    {

        return $this->facebookApi;
    }

    /**
     * @return int
     * @author jonathanb
     * @since 2012-09-14
     */
    public function getMe()
    {

        return $this->facebookApi->api('/me');
    }

    /**
     * @return array
     * @author jonathanb
     * @since 2012-09-14
     */
    public function getFriends()
    {
        $friends = $this->facebookApi->api('/me/friends&fields=id,name,location');
        $friends = $friends['data'];

        foreach ($friends as $key => $friend) {
            if (array_key_exists('location', $friend) && !empty($friends[$key]['location']['name'])) {
                $location = $this->getLocation($friends[$key]['location']['name']);
                if ($location) {
                    $friends[$key]['location']['lat'] = $location->getLat();
                    $friends[$key]['location']['lng'] = $location->getLng();
                }
            }
        }

        return $friends;
    }

    /**
     * @param string $name
     * @return Location
     * @author jonathanb
     * @since 2012-09-14
     */
    public function getLocation($name)
    {
        $location = $this->getLocationFromCache($name);
        if ($location == null) {
            $location = $this->getLocationFromGoogle($name);
            $this->cacheLocation($location);
        }

        return $location;
    }

    /**
     * @param string $name
     * @return Location
     * @author jonathanb
     * @since 2012-09-14
     */
    public function getLocationFromCache($name)
    {
        if (null == $name || empty($name)) {

        	return null;
        }

        return $this->dm->getRepository('TheodoMapBundle:Location')->findOneByName($name);
    }

    /**
     * @param Location $location
     * @author fabriceb
     * @since 2012-09-17
     */
    public function cacheLocation(Location $location)
    {
    	$this->dm->persist($location);
        $this->dm->flush();
	}

    /**
     * @param string $name
     * @return Location
     * @author jonathanb
     * @since 2012-09-16
     */
    public function getLocationFromGoogle($name)
    {
        $geocodeJson = file_get_contents('http://maps.googleapis.com/maps/api/geocode/json?address=' . urlencode($name) . '&sensor=false');
        $geocode = json_decode($geocodeJson, true);
        // We check if the geocode returned a result
        if (0 == count($geocode['results'])) {

        	return null;
        }
        $geocodeLocation = $geocode['results'][0]['geometry']['location'];

        return new Location($name, $geocodeLocation['lat'], $geocodeLocation['lng']);
    }
}


