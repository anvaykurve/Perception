import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
import numpy as np
from sklearn.cluster import DBSCAN

class ConeCentroidPublisher(Node):
    def __init__(self):
        super().__init__('cone_centroid_publisher')
        
        # 1. SUBSCRIBER: Listen to the raw LiDAR
        self.subscription = self.create_subscription(
            PointCloud,
            '/carmaker/pointcloud', 
            self.cloud_callback,
            1
        )
        
        # 2. PUBLISHER: Output ONLY the calculated centroids
        self.centroid_publisher = self.create_publisher(PointCloud, '/cone_centroids', 10)
        self.get_logger().info("Centroid clustering node started. Requiring 50 points per cone.")

    def cloud_callback(self, msg):
        ground_z_threshold = -0.4 
        valid_points = []
        
        # Filter the ground
        for p in msg.points:
            if p.z > ground_z_threshold:
                valid_points.append([p.x, p.y, p.z])

        centroid_msg = PointCloud()
        centroid_msg.header = msg.header 
        
        # DBSCAN Clustering
        if len(valid_points) > 0:
            points_np = np.array(valid_points)
            
            # min_samples=50 guarantees that only groups with at least 50 points are considered a cone
            # eps=0.5 sets the maximum distance (in meters) between points to be grouped together
            dbscan = DBSCAN(eps=0.5, min_samples=50)
            labels = dbscan.fit_predict(points_np)
            
            unique_labels = set(labels)
            
            # Calculate and store the centroid for each valid cluster
            for label in unique_labels:
                if label == -1:
                    continue  # -1 represents rejected noise (clusters with fewer than 50 points)
                
                # Extract all X, Y, Z coordinates belonging to this specific cone
                cluster_points = points_np[labels == label]
                
                # Calculate the centroid (the mean average of X, Y, and Z)
                centroid_coords = np.mean(cluster_points, axis=0)
                
                # Create a Point32 object for the centroid
                center_point = Point32()
                center_point.x = float(centroid_coords[0])
                center_point.y = float(centroid_coords[1])
                center_point.z = float(centroid_coords[2])
                
                # Add it to our outgoing message
                centroid_msg.points.append(center_point)
                
        # 3. PUBLISH: Send out the cloud containing only the centroid points
        self.centroid_publisher.publish(centroid_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ConeCentroidPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()