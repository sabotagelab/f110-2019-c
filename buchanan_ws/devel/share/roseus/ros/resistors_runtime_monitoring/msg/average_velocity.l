;; Auto-generated. Do not edit!


(when (boundp 'resistors_runtime_monitoring::average_velocity)
  (if (not (find-package "RESISTORS_RUNTIME_MONITORING"))
    (make-package "RESISTORS_RUNTIME_MONITORING"))
  (shadow 'average_velocity (find-package "RESISTORS_RUNTIME_MONITORING")))
(unless (find-package "RESISTORS_RUNTIME_MONITORING::AVERAGE_VELOCITY")
  (make-package "RESISTORS_RUNTIME_MONITORING::AVERAGE_VELOCITY"))

(in-package "ROS")
;;//! \htmlinclude average_velocity.msg.html


(defclass resistors_runtime_monitoring::average_velocity
  :super ros::object
  :slots (_average ))

(defmethod resistors_runtime_monitoring::average_velocity
  (:init
   (&key
    ((:average __average) 0.0)
    )
   (send-super :init)
   (setq _average (float __average))
   self)
  (:average
   (&optional __average)
   (if __average (setq _average __average)) _average)
  (:serialization-length
   ()
   (+
    ;; float64 _average
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _average
       (sys::poke _average (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _average
     (setq _average (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get resistors_runtime_monitoring::average_velocity :md5sum-) "711be0a796b85a8a1e109ae6a26ad085")
(setf (get resistors_runtime_monitoring::average_velocity :datatype-) "resistors_runtime_monitoring/average_velocity")
(setf (get resistors_runtime_monitoring::average_velocity :definition-)
      "float64 average

")



(provide :resistors_runtime_monitoring/average_velocity "711be0a796b85a8a1e109ae6a26ad085")


