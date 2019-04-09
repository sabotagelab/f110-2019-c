
(cl:in-package :asdf)

(defsystem "buchanan_runtime_monitoring-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "average" :depends-on ("_package_average"))
    (:file "_package_average" :depends-on ("_package"))
  ))