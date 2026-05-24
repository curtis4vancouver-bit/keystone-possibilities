-- PASTE THIS ENTIRE THING INTO SUPABASE SQL EDITOR AND CLICK "RUN"
-- This fixes the broken trigger and automates your PM account setup upon signup

-- Step 1: Repair the public.users insert mapping function
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, full_name, role, is_approved)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', 'New User'),
    CASE WHEN NEW.email = 'curtis4vancouver@gmail.com' THEN 'pm'::user_role ELSE 'trade'::user_role END,
    CASE WHEN NEW.email = 'curtis4vancouver@gmail.com' THEN true ELSE false END
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Step 2: Drop the old trigger if it exists to avoid conflicts
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Step 3: Recreate the trigger bound to auth.users insertions
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
