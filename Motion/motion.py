import sys
import time
import qi


class FollowingBuddy:
    """Pepper has a built-in face tracker and movement follower."""

    # Try changing your __init__ connection sequence to this style:
    def __init__(self, ip: str = "172.17.10.113", port: str = "9559"):
        self.ip = ip
        self.connection_url = f"tcp://{self.ip}:{port}"

        # Passing the URL directly via sys.argv equivalents to the Qi App
        self.app = qi.Application(["FollowingBuddy", "--qi-url=" + self.connection_url])
        
        try:
            self.app.start()
            self.session = self.app.session
            print(f"Successfully connected to Pepper at {self.connection_url}")
            
            self.motion = self.session.service("ALMotion")
            self.tracker = self.session.service("ALTracker")
            self.awareness = self.session.service("ALBasicAwareness")
        except Exception as e:
            print(f"Could not connect to Pepper: {e}")
            sys.exit(1)

    def follow_user(self):
        # 1. Wake up Pepper and enable motor stiffness
        self.motion.wakeUp()

        target_name = "Face"
        face_width = 0.15  # Target size in meters for distance estimation

        # 2. Register the face as our tracking target
        self.tracker.registerTarget(target_name, face_width)

        # 3. Set to "Move" mode (forces head look + base movement to follow)
        self.tracker.setMode("Move")

        # Configure positioning: Keep Pepper 1.0m away, perfectly centered
        self.tracker.setRelativePosition([1.0, 0.0, 0.0, 0.1])

        # 4. Turn off basic awareness so it doesn't fight our tracker
        self.toggle_awareness(False)

        # 5. Start the native tracking loop
        self.tracker.track(target_name)
        print("Face tracking and following activated. Press Ctrl+C to stop.")

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping tracker safely...")
            self.tracker.stopTracker()
            self.tracker.unregisterTarget(target_name)

            # 6. Restore Pepper's default state on exit
            self.toggle_awareness(True)
            # self.motion.rest() # Uncomment if you want Pepper to go to sleep on exit

    def toggle_awareness(self, toggle: bool = False):
        """Helper to turn autonomous awareness behaviors on or off."""
        print(f"Setting ALBasicAwareness to: {toggle}")
        self.awareness.setEnabled(toggle)


if __name__ == "__main__":
    # The main block becomes beautifully simple and safer
    buddy = FollowingBuddy()
    buddy.follow_user()