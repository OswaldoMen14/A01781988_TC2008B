using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lerp301 : MonoBehaviour
{

    [SerializeField] Vector3 startPos;
    [SerializeField] Vector3 finalPos;
    [Range(0.0f, 1.0f)]
    [SerializeField] float t;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 position = startPos + (finalPos - startPos) * t;
        //Using the Unity transforms
        transform.position = position;
    }
}
