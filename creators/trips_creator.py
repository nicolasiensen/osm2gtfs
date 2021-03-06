# coding=utf-8


class TripsCreator(object):

    def __init__(self, config):
        self.config = config

    def __repr__(self):
        rep = ""
        if self.config is not None:
            rep += str(self.config) + " | "
        return rep

    def add_trips_to_schedule(self, schedule, data):
        raise NotImplementedError("Should have implemented this")

    @staticmethod
    def interpolate_stop_times(trip):
        """
        interpolate stop_times, because Navitia does not handle this itself by now
        """
        for secs, stop_time, is_timepoint in trip.GetTimeInterpolatedStops():
            if not is_timepoint:
                stop_time.arrival_secs = secs
                stop_time.departure_secs = secs
                trip.ReplaceStopTimeObject(stop_time)

    @staticmethod
    def add_shape(schedule, route_id, osm_r):
        """
        create GTFS shape and return shape_id to add on GTFS trip
        """
        import transitfeed
        shape_id = str(route_id)
        try:
            schedule.GetShape(shape_id)
        except KeyError:
            shape = transitfeed.Shape(shape_id)
            for point in osm_r.shape:
                shape.AddPoint(
                    lat=float(point["lat"]), lon=float(point["lon"]))
            schedule.AddShapeObject(shape)
        return shape_id
