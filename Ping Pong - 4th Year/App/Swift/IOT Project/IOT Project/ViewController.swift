//
//  ViewController.swift
//  IOT Project
//
//  Created by Roberto Pop, Ogo Onfuwa, Max Amrabure, Jack Hand on 17/02/2022.
//

import UIKit
import CoreMotion


struct Response: Codable {
    let x: String
    let y: String
    let z: String
}


class ViewController: UIViewController {
    
    private func getData(from url: URL, xValue: String, yValue: String, zValue: String) {
        
        var request = URLRequest(url: url)
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.httpMethod = "POST"
        
        
        let body = ["player2_x": xValue, "player2_y": yValue, "player2_z": zValue]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: [])
        
        
        URLSession.shared.dataTask(with: request) {data, response, error in
            
            guard let data = data, error == nil else {
                print("error retrieving products")
                return
            }
            
            var dataRetrieved: Response?
            do {
                dataRetrieved = try JSONDecoder().decode(Response.self, from: data)
            }
            catch {
                print(String(describing: error))
            }
            
            guard let json = dataRetrieved else {
                return
            }
            
            print(json)
            
        }.resume()
        
    }

    //Player1 Data Labals - Gyroscope
    @IBOutlet weak var xLabel: UILabel!
    @IBOutlet weak var yLabel: UILabel!
    @IBOutlet weak var zLabel: UILabel!
    
    //Player2 Data Labels - Gyroscope
    @IBOutlet weak var xGyro: UILabel!
    @IBOutlet weak var yGyro: UILabel!
    @IBOutlet weak var zGyro: UILabel!
    
    let motionData = CMMotionManager()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        func POST_Player1(x: Double, y:Double, z:Double) {
            guard let url = URL(string: "http://192.168.0.17:8000/update_player1_data/") else {
                return
            }
            let x = String(x)
            let y = String(y)
            let z = String(z)
            
            self.getData(from: url, xValue: x, yValue: y, zValue: z)
        }
        
        func POST_Player2(x: Double, y:Double, z:Double) {
            guard let url = URL(string: "http://192.168.0.17:8000/update_player2_data/") else {
                return
            }
            let x = String(x)
            let y = String(y)
            let z = String(z)
            
            self.getData(from: url, xValue: x, yValue: y, zValue: z)
        }
        
        motionData.startAccelerometerUpdates()
        motionData.accelerometerUpdateInterval = 0.2
        
        motionData.startGyroUpdates()
        motionData.gyroUpdateInterval = 0.2
        
        var Acceleration_x = 1.0
        var Acceleration_y = 1.0
        var Acceleration_z = 1.0
        
        Timer.scheduledTimer(withTimeInterval: 0.2, repeats: true) { _ in
            
            if let xData = self.motionData.accelerometerData {
                if(self.xLabel != nil) {
                    self.xLabel?.text = String(xData.acceleration.x)
                    self.yLabel?.text = String(xData.acceleration.y)
                    self.zLabel?.text = String(xData.acceleration.z)
                    Acceleration_x = Double(xData.acceleration.x)
                    Acceleration_y = Double(xData.acceleration.y)
                    Acceleration_z = Double(xData.acceleration.z)
                }
                else {
                    self.motionData.stopAccelerometerUpdates()
                    let num = "0"
                    self.xLabel?.text = "\(num)"
                    self.yLabel?.text = "\(num)"
                    self.zLabel?.text = "\(num)"
                }
            }
            
            if let gyroDataPlayer2 = self.motionData.gyroData {
            
                if(self.xGyro != nil) {
                    self.xGyro?.text = String(gyroDataPlayer2.rotationRate.x)
                    self.yGyro?.text = String(gyroDataPlayer2.rotationRate.y)
                    self.zGyro?.text = String(gyroDataPlayer2.rotationRate.z)
                    
                    let x = (1 + (Double(gyroDataPlayer2.rotationRate.x) + Acceleration_x) - 1)
                    let y = (1 + (Double(gyroDataPlayer2.rotationRate.y) + Acceleration_y) - 1)
                    let z = (1 + (Double(gyroDataPlayer2.rotationRate.z) + Acceleration_z) - 1)
                    
                    
                    POST_Player2(x: Double(x), y: Double(y), z: Double(z))
                }
                else {
                    self.motionData.stopGyroUpdates()
                    let num = "0"
                    self.xGyro?.text = "\(num)"
                    self.yGyro?.text = "\(num)"
                    self.zGyro?.text = "\(num)"
                }
            }
            
        }
    }
}

