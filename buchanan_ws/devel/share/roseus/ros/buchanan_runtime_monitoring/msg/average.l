;; Auto-generated. Do not edit!


(when (boundp 'buchanan_runtime_monitoring::average)
  (if (not (find-package "BUCHANAN_RUNTIME_MONITORING"))
    (make-package "BUCHANAN_RUNTIME_MONITORING"))
  (shadow 'average (find-package "BUCHANAN_RUNTIME_MONITORING")))
(unless (find-package "BUCHANAN_RUNTIME_MONITORING::AVERAGE")
  (make-package "BUCHANAN_RUNTIME_MONITORING::AVERAGE"))

(in-package "ROS")
;;//! \htmlinclude average.msg.html


(defclass buchanan_runtime_monitoring::average
  :super ros::object
  :slots (_average ))

(defmethod buchanan_runtime_monitoring::average
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
    ;; float32 _average
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _average
       (sys::poke _average (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _average
     (setq _average (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get buchanan_runtime_monitoring::average :md5sum-) "26f1aeb3d6aa6d8e4617861692487d73")
(setf (get buchanan_runtime_monitoring::average :datatype-) "buchanan_runtime_monitoring/average")
(setf (get buchanan_runtime_monitoring::average :definition-)
      "float32 average

")



(provide :buchanan_runtime_monitoring/average "26f1aeb3d6aa6d8e4617861692487d73")


