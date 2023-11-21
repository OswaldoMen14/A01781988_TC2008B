/*
Functions to work with wheels and car transformation / rotation

Oswaldo Ilhuicatzi Mendizábal with the help of Alan with understanding the system
2023-11-16
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Appy_Transforms : MonoBehaviour
{
    [SerializeField] Vector3 displacement; // Translation vector
    [SerializeField] float speed;           // Rotation speed
    [SerializeField] GameObject wheel;     // Wheel object
    [SerializeField] float angle;          // Rotation angle
    [SerializeField] AXIS rotationAxis;    // Rotation axis
    [SerializeField] Vector3[] wheelPos;   // Positions of multiple wheels

    Mesh mesh;
    Mesh[] wheelMesh = new Mesh[4];
    Vector3[][] wheelVertex = new Vector3[4][];
    Vector3[][] wheelNewVertex = new Vector3[4][];
    Vector3[] baseVertex;
    Vector3[] newVertex;

    void Start()
    {
        // Get the mesh and vertices of the main object
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertex = mesh.vertices;
        newVertex = new Vector3[baseVertex.Length];
        for (int i = 0; i < baseVertex.Length; i++)
        {
            newVertex[i] = baseVertex[i];
        }
        generateWheels();
    }

    void Update()
    {
        // Calculate rotation angle based on displacement
        angle = GetAngle(displacement);
        DoTransform();
    }

    // Calculate the rotation angle based on the displacement vector
    float GetAngle(Vector3 displacement)
    {
        return Mathf.Atan2(displacement.z, -displacement.x) * Mathf.Rad2Deg;
    }

    // Apply transformations to the main object and wheels
    void DoTransform()
    {
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time,
            displacement.y * Time.time,
            displacement.z * Time.time);

        Matrix4x4 rotate = HW_Transforms.RotateMat(angle, rotationAxis);

        Matrix4x4 composite = move * rotate;

        Matrix4x4 rotateWheel = HW_Transforms.RotateMat(Time.time * speed, AXIS.Z);

         // Apply transformations to each wheel
        for (int i = 0; i < wheelMesh.Length; i++)
        {
            Matrix4x4 mainWheelPos = HW_Transforms.TranslationMat(wheelPos[i].x, wheelPos[i].y, wheelPos[i].z);
            Matrix4x4 wheelComp = composite * mainWheelPos * rotateWheel;

            for (int j = 0; j < wheelNewVertex[i].Length; j++)
            {
                Vector4 temp = new Vector4(wheelVertex[i][j].x, wheelVertex[i][j].y, wheelVertex[i][j].z, 1);
                wheelNewVertex[i][j] = wheelComp * temp;
            }

            wheelMesh[i].vertices = wheelNewVertex[i];
            wheelMesh[i].RecalculateNormals();
        }

        // Apply transformations to each vertex of the main object
        for (int i = 0; i < newVertex.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertex[i].x, baseVertex[i].y, baseVertex[i].z, 1);
            newVertex[i] = composite * temp;
        }

        mesh.vertices = newVertex;
        mesh.RecalculateNormals();
    }

    // Generate multiple wheels according to the car´s position
    void generateWheels()
    {
        Vector3 originalPos = new Vector3(0, 0, 0);
        for (int i = 0; i < wheelPos.Length; i++)
        {
            GameObject newTemp = Instantiate(wheel, originalPos, Quaternion.identity);
            wheelMesh[i] = newTemp.GetComponentInChildren<MeshFilter>().mesh;
            wheelVertex[i] = wheelMesh[i].vertices;
            wheelNewVertex[i] = new Vector3[wheelVertex[i].Length];
            for (int j = 0; j < wheelVertex[i].Length; j++)
            {
                wheelNewVertex[i][j] = wheelVertex[i][j];
            }
        }
    }
}
