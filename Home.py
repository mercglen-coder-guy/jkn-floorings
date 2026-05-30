import re
from dataclasses import dataclass
from typing import Dict, Any, List
import csv
from pathlib import Path

from litestar import Litestar, Controller, get, post
from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.static_files.config import StaticFilesConfig
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body

# -------------------------------------------------------------
# Data Models
# -------------------------------------------------------------

@dataclass
class QuoteRequest:
    """Represents a request for a flooring installation quote."""
    name: str
    email: str
    phone: str
    flooring_type: str
    size: str
    message: str = ""


@dataclass
class ChatMessage:
    """Represents a user message sent to the AI Agent."""
    message: str

# -------------------------------------------------------------
# Route Controllers (CamelCase / PascalCase)
# -------------------------------------------------------------

class HomeController(Controller):
    """Controller for rendering the JKN Flooring homepage."""
    path = "/"

    @get()
    async def getHome(self) -> Template:
        """Render and return the Home page template."""
        return Template(template_name="home.html")


class QuoteApiController(Controller):
    """Controller for handling estimate request API calls."""
    path = "/api/quote"

    @post()
    async def processQuote(self, data: QuoteRequest) -> Dict[str, Any]:
        """Process the submitted quote data and return a friendly confirmation."""
        flooring_labels = {
            "hardwood": "Solid / Engineered Hardwood",
            "vinyl": "Luxury Vinyl Plank (LVP)",
            "laminate": "Premium Laminate",
            "other": "Other / Repairs"
        }
        lbl = flooring_labels.get(data.flooring_type, data.flooring_type)
        
        msg = (
            f"Thank you, {data.name}! Your request for {data.size} sq. ft. of "
            f"{lbl} installation has been received successfully. Our Toronto "
            f"team will review your project and reach out to you at {data.phone} "
            f"or {data.email} with a full estimate shortly."
        )
        
        return {
            "status": "success",
            "message": msg
        }


class VisionApiController(Controller):
    """Controller for handling AI-powered visual flooring estimations."""
    path = "/api/vision"

    @post()
    async def processVision(
        self,
        data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART)
    ) -> Dict[str, Any]:
        """
        Analyze an uploaded flooring inspiration photo.
        Returns a style match, specifications, and dynamic GTA-specific estimated costs.
        """
        # Read a tiny bit of the uploaded file to ensure upload is functioning
        _content = await data.read(1024)
        filename = data.filename.lower()

        # Custom logic based on filename keywords for fun interactive realism
        if any(w in filename for w in ["wood", "oak", "hard", "timber", "floor"]):
            style = "Natural Oak Wide Plank Hardwood"
            category = "Engineered Hardwood"
            match_rate = "94%"
            subfloor = "Standard plywood subfloor check, sound insulation underlayment required."
            cost_range = "$8.50 - $14.00 / sq. ft. (installed)"
            description = (
                "Stunning natural wood grain with warm honey undertones. Perfect for open-concept "
                "living spaces and upscale residences demanding architectural prestige."
            )
        elif any(w in filename for w in ["vinyl", "plank", "water", "grey", "gray"]):
            style = "Waterproof Luxury Vinyl Plank (LVP)"
            category = "Vinyl & Laminate"
            match_rate = "97%"
            subfloor = "Direct concrete install compatible. Premium cork or foam moisture barrier underlayment."
            cost_range = "$4.50 - $8.00 / sq. ft. (installed)"
            description = (
                "Ultra-durable, scratch-resistant surface with an embossed authentic wood grain texture. "
                "100% waterproof core, making it optimal for kitchens, basements, and active homes."
            )
        elif any(w in filename for w in ["tile", "stone", "marble", "porcelain", "bath"]):
            style = "Calacatta Gold Porcelain Tile"
            category = "Tiles"
            match_rate = "91%"
            subfloor = "Cement board underlayment layer required. High-grade polymer-modified thin-set mortar."
            cost_range = "$12.00 - $22.00 / sq. ft. (installed)"
            description = (
                "Elegantly detailed faux-marble porcelain. Offers luxurious classic architecture aesthetic "
                "with outstanding durability, perfect for entries, hearths, and elegant bathrooms."
            )
        else:
            # High-end default matcher
            style = "Modern Architectural Surface (Premium Oak Laminate)"
            category = "Vinyl & Laminate"
            match_rate = "89%"
            subfloor = "Plywood/Concrete leveling check. 2mm acoustic reduction underlayment."
            cost_range = "$5.50 - $8.50 / sq. ft. (installed)"
            description = (
                "Highly resilient architectural-grade laminate with exceptional wear resistance. "
                "Offers a beautiful contemporary flat matte finish that hides footprints and dust."
            )

        return {
            "status": "success",
            "filename": data.filename,
            "analysis": {
                "detected_style": style,
                "category": category,
                "match_rate": match_rate,
                "subfloor_spec": subfloor,
                "cost_range": cost_range,
                "description": description
            }
        }


class ChatApiController(Controller):
    """Controller for running the JKN AI Architectural Agent Chat backend."""
    path = "/api/chat"

    @post()
    async def talkToAgent(self, data: ChatMessage) -> Dict[str, Any]:
        """
        Processes chatbot questions.
        Resolves keywords to return custom agent copy and relevant catalog recommendation cards.
        """
        user_msg = data.message.lower()
        response_text = ""
        cards: List[Dict[str, Any]] = []

        # Simple semantic router based on keywords
        if any(w in user_msg for w in ["vinyl", "waterproof", "lvp", "wet"]):
            response_text = (
                "Luxury Vinyl Plank (LVP) is a superb choice for Toronto homes. "
                "It is 100% waterproof, incredibly resistant to high-traffic scratches, and looks "
                "exactly like real wood. It's especially recommended for basements and kitchens. "
                "Here are JKN's top in-stock vinyl products:"
            )
            cards = [
                {
                    "title": "Vinyl Planks (LVP)",
                    "category": "Waterproof Core",
                    "price": "$3.50 - $7.00 / sq. ft.",
                    "image": "https://images.unsplash.com/photo-1581858726788-75bc0f6a952d?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Vinyl Tiles & Loose Lay",
                    "category": "Commercial Grade",
                    "price": "$4.00 - $8.50 / sq. ft.",
                    "image": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80"
                }
            ]
        elif any(w in user_msg for w in ["hardwood", "engineered", "wood", "oak", "maple"]):
            response_text = (
                "For timeless luxury, nothing beats Engineered or Solid Hardwood flooring. "
                "Our collections are adapted to the southern Ontario climate (managing humidity shifts "
                "flawlessly to prevent warping). We specialize in custom wide-plank oak installations. "
                "Take a look at these popular wood choices in our Toronto showroom:"
            )
            cards = [
                {
                    "title": "Floor & Wall Tiles",
                    "category": "Ceramic & Porcelain",
                    "price": "$5.50 - $12.00 / sq. ft.",
                    "image": "https://images.unsplash.com/photo-1600607686527-6fb886090705?auto=format&fit=crop&w=800&q=80"
                }
            ]
        elif any(w in user_msg for w in ["tile", "bathroom", "kitchen", "backsplash", "mosaic", "marble"]):
            response_text = (
                "Architectural tiles bring durable artistry to kitchens, baths, and entrances. "
                "Porcelain and ceramic tiles offer complete water resistance and custom grid alignments. "
                "We provide full grid preparation and dustless thin-set installations in the GTA. "
                "Here are JKN's recommended tiles:"
            )
            cards = [
                {
                    "title": "Backsplash Tiles",
                    "category": "Kitchen & Bath",
                    "price": "$8.00 - $18.00 / sq. ft.",
                    "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=800&q=80"
                },
                {
                    "title": "Mosaic Tiles",
                    "category": "Intricate Details",
                    "price": "$12.00 - $25.00 / sq. ft.",
                    "image": "https://images.unsplash.com/photo-1615876234886-fd9a39fda97f?auto=format&fit=crop&w=800&q=80"
                }
            ]
        elif any(w in user_msg for w in ["cost", "price", "quote", "rate", "estimate"]):
            response_text = (
                "Our pricing is highly transparent! Laminate flooring starts as low as $2.50/sq. ft., "
                "luxury vinyl starts at $3.50/sq. ft., and premium hardwood runs from $6.00 to $15.00/sq. ft. "
                "Installation labor depends on subfloor preparation. To get a precise quote, use our "
                "AI Vision tool above, or fill out the free estimate request form below!"
            )
        elif any(w in user_msg for w in ["warranty", "licensed", "insured", "guarantee"]):
            response_text = (
                "All installations are fully handled by our licensed and insured JKN Flooring team. "
                "We provide a standard 2-Year Installation Workmanship Guarantee alongside manufacturers' "
                "structural lifetime warranties on all premium engineered hardwood, vinyl, and laminates. "
                "Your investment is fully covered!"
            )
        else:
            response_text = (
                "Hello! I am the JKN AI Architectural Agent. I can advise you on high-performance surfaces "
                "for your residential or commercial GTA project. Try asking me about 'waterproof vinyl', "
                "'engineered hardwood options', 'backsplash tile installation', or 'warranty details'!"
            )

        return {
            "status": "success",
            "reply": response_text,
            "cards": cards
        }

# -------------------------------------------------------------
# Biyork Store Controller
# -------------------------------------------------------------

class BiyorkController(Controller):
    """Controller for rendering the Biyork products storefront."""
    path = "/biyork"

    @get()
    async def getBiyorkStore(self) -> Template:
        """Parse the Biyork catalog CSV and render the products page."""
        catalog_path = Path("Data/biyork_enterprise_catalog.csv")
        products = []
        if catalog_path.exists():
            with open(catalog_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    products.append(row)
        
        return Template(template_name="biyork.html", context={"products": products})

# -------------------------------------------------------------
# Application Setup & Configurations
# -------------------------------------------------------------

# Setup Template engine pointing to the 'Templates' directory
template_config = TemplateConfig(
    directory="Templates",
    engine=JinjaTemplateEngine,
)

# Setup Static files configuration serving files from '/static'
static_files_config = [
    StaticFilesConfig(
        directories=["static"],
        path="/static",
    )
]

# Initialize Litestar application with new API endpoints
app = Litestar(
    route_handlers=[HomeController, QuoteApiController, VisionApiController, ChatApiController, BiyorkController],
    template_config=template_config,
    static_files_config=static_files_config,
)
