from qdrant_client import QdrantClient

def find_panic_point():
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "keystone_unified"
    
    start_offset = "1f9928b2-8703-4e4d-ab89-3d7915945b8f"
    print(f"Stepping through points starting from offset {start_offset}...")
    
    offset = start_offset
    step = 1
    
    while step <= 250:
        try:
            res, next_offset = client.scroll(
                collection_name=collection_name,
                limit=1,
                with_payload=True,
                with_vectors=True, # let's fetch vectors too to see if the vector itself is the issue
                offset=offset
            )
            
            if not res:
                print(f"Step {step}: No points returned. Reached end.")
                break
                
            point = res[0]
            print(f"Step {step}: Point ID={point.id} successfully loaded.")
            
            if next_offset is None:
                print("Reached end (next_offset is None)")
                break
                
            offset = next_offset
            step += 1
            
        except Exception as e:
            print(f"\nCRITICAL: Step {step} failed (current offset={offset}): {e}")
            
            # Let's try loading without vectors
            print("Trying load without vectors...")
            try:
                res_no_vec, _ = client.scroll(
                    collection_name=collection_name,
                    limit=1,
                    with_payload=True,
                    with_vectors=False,
                    offset=offset
                )
                print(f"  Success without vectors! Point ID: {res_no_vec[0].id if res_no_vec else 'None'}")
            except Exception as e_no_vec:
                print(f"  Failed without vectors too: {e_no_vec}")
                
            # Let's try loading without payload
            print("Trying load without payload...")
            try:
                res_no_pay, _ = client.scroll(
                    collection_name=collection_name,
                    limit=1,
                    with_payload=False,
                    with_vectors=True,
                    offset=offset
                )
                print(f"  Success without payload! Point ID: {res_no_pay[0].id if res_no_pay else 'None'}")
            except Exception as e_no_pay:
                print(f"  Failed without payload too: {e_no_pay}")
                
            break

if __name__ == "__main__":
    find_panic_point()
