; Auto-generated. Do not edit!


(cl:in-package resistors_runtime_monitoring-msg)


;//! \htmlinclude average_velocity.msg.html

(cl:defclass <average_velocity> (roslisp-msg-protocol:ros-message)
  ((average
    :reader average
    :initarg :average
    :type cl:float
    :initform 0.0))
)

(cl:defclass average_velocity (<average_velocity>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <average_velocity>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'average_velocity)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name resistors_runtime_monitoring-msg:<average_velocity> is deprecated: use resistors_runtime_monitoring-msg:average_velocity instead.")))

(cl:ensure-generic-function 'average-val :lambda-list '(m))
(cl:defmethod average-val ((m <average_velocity>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader resistors_runtime_monitoring-msg:average-val is deprecated.  Use resistors_runtime_monitoring-msg:average instead.")
  (average m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <average_velocity>) ostream)
  "Serializes a message object of type '<average_velocity>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'average))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <average_velocity>) istream)
  "Deserializes a message object of type '<average_velocity>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'average) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<average_velocity>)))
  "Returns string type for a message object of type '<average_velocity>"
  "resistors_runtime_monitoring/average_velocity")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'average_velocity)))
  "Returns string type for a message object of type 'average_velocity"
  "resistors_runtime_monitoring/average_velocity")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<average_velocity>)))
  "Returns md5sum for a message object of type '<average_velocity>"
  "711be0a796b85a8a1e109ae6a26ad085")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'average_velocity)))
  "Returns md5sum for a message object of type 'average_velocity"
  "711be0a796b85a8a1e109ae6a26ad085")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<average_velocity>)))
  "Returns full string definition for message of type '<average_velocity>"
  (cl:format cl:nil "float64 average~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'average_velocity)))
  "Returns full string definition for message of type 'average_velocity"
  (cl:format cl:nil "float64 average~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <average_velocity>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <average_velocity>))
  "Converts a ROS message object to a list"
  (cl:list 'average_velocity
    (cl:cons ':average (average msg))
))
