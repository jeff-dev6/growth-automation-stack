from PIL import Image, UnidentifiedImageError
from pathlib import Path
from core.logger import get_logger

log = get_logger("generate_image_content")

class ImageContentGenerator:
    """
    Service for image manipulation, 
    specifically designed for automated branding and watermarking.
    """

    @staticmethod
    def calculate_position(background_size: tuple, logo_size: tuple, offset=(20, 20), anchor="bottom-right") -> tuple:
        """
        Pure math function to calculate logo position on the background image.
        
        Args:
            background_size (tuple): Size of the background image (width, height).
            logo_size (tuple): Size of the logo image (width, height).
            offset (tuple): offset from the anchor point (offset_x, offset_y).
            anchor (str): Anchor position for the logo ("bottom-right", "bottom-left", "top-right", "top-left").

        Returns:
            tuple: Calculated (x, y) position for the logo.
        """

        background_width, background_height = background_size
        logo_width, logo_height = logo_size
        offset_x, offset_y = offset

        if anchor == "bottom-right":
            return (background_width - logo_width - offset_x, background_height - logo_height - offset_y)
        elif anchor == "bottom-left":
            return (offset_x, background_height - logo_height - offset_y)
        elif anchor == "top-right":
            return (background_width - logo_width - offset_x, offset_y)
        elif anchor == "top-left":
            return (offset_x, offset_y)
        else:
            return ((background_width - logo_width) // 2, (background_height - logo_height) // 2)
        

    @classmethod
    def render_image(cls, background_input: str, logo_input: str, output_input: str, offset=(20, 20), anchor="bottom-right") -> None:
        """
        Overlays a logo onto a background image and saves the result.

        Args:
            background_path (str or Path): Path to the background image.
            logo_path (str or Path): Path to the logo image.
            output_path (str or Path): Path to save the resulting image.
            offset (tuple): offset from the anchor point (offset_x, offset_y).
            anchor (str): Anchor position for the logo ("bottom-right", "bottom-left", "top-right", "top-left").

        Returns:
            None
        """

        # 1. Path Resolution (Converts names to full system paths)
        # If you aren't using a config file yet, Path(background_input) works fine.
        background_path = Path(background_input)
        logo_path = Path(logo_input)
        output_path = Path(output_input)

        ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp",}

        try:

            # Hard Pre-Flight Checks (Stop early if something is wrong)
            for file in [background_path, logo_path]:
                if not file.exists():
                    raise FileNotFoundError(f"File not found: {file.absolute()}")
                if file.suffix.lower() not in ALLOWED_EXTENSIONS:
                    raise ValueError(f"Unsupported format: {file.suffix} for file {file.name}")

            # Ensure output folder exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            

            # Load images and convert to RGBA for transparency handling
            with Image.open(background_path) as background_image, Image.open(logo_path) as logo_image:
                background = background_image.convert("RGBA")
                logo = logo_image.convert("RGBA")

                # Auto-Scaling logic
                background_width, background_height = background.size
                max_w, max_h = background_width * 0.2, background_height * 0.2
                if logo.width > max_w or logo.height > max_h:

                    log.info("Logo exceeds background size, Auto-scaling to 20% of background size...")

                    scale = min(max_w / logo.width, max_h / logo.height)
                    new_logo_size = (int(logo.width * scale), int(logo.height * scale))
                    logo = logo.resize(new_logo_size, Image.Resampling.LANCZOS)

                    log.info(f"Logo resized to: {logo.width}x{logo.height}")
                    
                # Use our helper for positioning
                position = cls.calculate_position(background.size, logo.size, offset, anchor)

                # Paste using alpha channel as mask
                background.paste(logo, position, logo)
                    
                # Convert to RGB (removes transparency for JPG support) and save
                final_image = background.convert("RGB")
                final_image.save(output_path)

                log.info(f"Successfully saved branded image to {output_path}")

        #Specific Error Safety Net
        except FileNotFoundError as e:
            log.error(f"PATH ERROR: {e}")
        except UnidentifiedImageError:
            log.error(f"INVALID IMAGE: Could not read {background_path.name} or {logo_path.name}")
        except PermissionError:
            log.error(f"PERMISSION ERROR: Is {output_path.name} open in another program?")
        except Exception as e:
            log.error(f"CRITICAL ERROR in render_image: {e}")
            raise

    
        


